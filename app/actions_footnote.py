"""اکشن‌های کارت «درج پانویس (پاورقی)»."""

import ctypes
from tkinter import messagebox

import customtkinter as ctk

try:
    from .glass_dropdown import GlassDropdown
except ImportError:
    from app.glass_dropdown import GlassDropdown


FOOTNOTE_MENU = [
    ("فارسی", None),
    ("انگلیسی", None),
]


class FootnoteActions:
    """مدیریت منو و تنظیمات اولیه زبان پانویس."""

    def footnote_menu_action(self, card):
        """باز و بسته کردن منوی کشویی پانویس."""

        # اگر منو باز است، آن را ببند
        if (
            hasattr(self, "_footnote_popup")
            and self._footnote_popup
            and self._footnote_popup.is_open
        ):
            self._footnote_popup.close()
            return

        try:
            scale = ctk.ScalingTracker.get_window_scaling(self)
        except Exception:
            scale = 1.0

        try:
            self._footnote_popup = GlassDropdown(
                self,
                card,
                FOOTNOTE_MENU,
                on_select=self._on_footnote_select,
                scale=scale,
            )
            self._footnote_popup.open()

        except Exception as error:
            messagebox.showerror(
                "خطا",
                f"باز کردن منوی پانویس با مشکل مواجه شد:\n{error}",
            )

    def _on_footnote_select(self, path):
        """مدیریت انتخاب زبان پانویس."""

        language = path[0]

        # ذخیره زبان انتخاب‌شده
        self.footnote_language = language

        # تنظیمات پیش‌فرض
        if not hasattr(self, "footnote_settings"):
            self.footnote_settings = {
                "auto_keyboard": True,
                "auto_direction": True,
                "default_language": "فارسی",
            }

        # تغییر زبان کیبورد
        if self.footnote_settings.get("auto_keyboard", True):
            self._switch_footnote_keyboard(language)

        # ایجاد پانویس در محل فعلی Cursor
        self._insert_footnote()

    
    def _insert_footnote(self):
        """ایجاد پانویس در محل فعلی Cursor سند Word."""

        try:
            self.engine.ensure_ready()

            word = self.engine.word
            document = word.ActiveDocument
            selection = word.Selection

            # محل فعلی Cursor در سند
            range_obj = selection.Range

            # ایجاد پانویس
            footnote = document.Footnotes.Add(
                Range=range_obj,
                Text="",
            )

            # بررسی تنظیمات نمایش شماره پانویس
            reference_style = self.footnote_settings.get(
                "reference_style",
                "پیش‌فرض"
            )

            if reference_style == "همراه با خط تیره":
                reference_range = footnote.Reference.Duplicate
                reference_range.Collapse(0)
                reference_range.InsertAfter("-")
            # Range مربوط به متن پانویس
            footnote_range = footnote.Range

            # تنظیم جهت نوشتار
            self._apply_footnote_direction(
                footnote_range.Paragraphs(1)
            )

            # قرار دادن Cursor داخل متن پانویس
            footnote_range.Collapse(0)
            footnote_range.Select()

        except Exception as error:
            messagebox.showerror(
                "درج پانویس",
                f"درج پانویس با مشکل مواجه شد:\n{error}",
            )


    def _switch_footnote_keyboard(self, language):
        """تغییر زبان کیبورد ویندوز به فارسی یا انگلیسی."""

        keyboard_layouts = {
            "فارسی": "00000429",
            "انگلیسی": "00000409",
        }

        layout_id = keyboard_layouts.get(language)

        if not layout_id:
            return

        try:
            user32 = ctypes.WinDLL("user32", use_last_error=True)

            user32.LoadKeyboardLayoutW.argtypes = [
                ctypes.c_wchar_p,
                ctypes.c_uint,
            ]
            user32.LoadKeyboardLayoutW.restype = ctypes.c_void_p

            user32.ActivateKeyboardLayout.argtypes = [
                ctypes.c_void_p,
                ctypes.c_uint,
            ]
            user32.ActivateKeyboardLayout.restype = ctypes.c_void_p

            # بارگذاری و فعال‌سازی چیدمان کیبورد
            keyboard_handle = user32.LoadKeyboardLayoutW(
                layout_id,
                0x00000001,
            )

            if not keyboard_handle:
                raise OSError("چیدمان زبان موردنظر در ویندوز پیدا نشد.")

            user32.ActivateKeyboardLayout(keyboard_handle, 0)

        except Exception as error:
            messagebox.showwarning(
                "تغییر زبان کیبورد",
                (
                    f"تغییر زبان کیبورد به «{language}» انجام نشد.\n\n"
                    "بررسی کن که چیدمان کیبورد این زبان در تنظیمات "
                    f"ویندوز نصب شده باشد.\n\nجزئیات: {error}"
                ),
            )

    def _apply_footnote_direction(self, paragraph):
        """اعمال جهت و تراز نوشتار متناسب با زبان پانویس."""

        if hasattr(self, "footnote_settings"):
            if not self.footnote_settings.get("auto_direction", True):
                return

        language = getattr(self, "footnote_language", "فارسی")

        if language == "فارسی":
            reading_order = 0  # RTL
            alignment = 2      # راست‌چین
        else:
            reading_order = 1  # LTR
            alignment = 0      # چپ‌چین

        paragraph.Range.ParagraphFormat.ReadingOrder = reading_order
        paragraph.Range.ParagraphFormat.Alignment = alignment
    
    
    def _apply_footnote_display_mode(self):
        """اعمال نحوه نمایش پانویس‌ها در سند Word."""

        try:
            self.engine.ensure_ready()

            document = self.engine.word.ActiveDocument

            display_mode = self.footnote_settings.get(
                "display_mode",
                "معمولی",
            )

            # تعیین تعداد ستون‌های پانویس
            columns = 2 if display_mode == "دو ستونه" else 1

            # اعمال تنظیم روی تمام بخش‌های سند
            for index in range(1, document.Sections.Count + 1):
                section = document.Sections(index)

                section.Range.FootnoteOptions.LayoutColumns = columns

        except Exception as error:
            messagebox.showerror(
                "تنظیم نحوه نمایش پانویس",
                f"اعمال تنظیمات پانویس با مشکل مواجه شد:\n{error}",
            )
    
    
    def _apply_footnote_separator_position(self):
        """اعمال موقعیت خط جداکننده پانویس در سند Word."""

        try:
            self.engine.ensure_ready()

            document = self.engine.word.ActiveDocument

            # دریافت موقعیت انتخاب‌شده در تنظیمات
            position = self.footnote_settings.get(
                "separator_position",
                "چپ"
            )

            # محاسبه عرض محدوده قابل نوشتن صفحه
            page_setup = document.Sections(1).PageSetup

            text_width = (
                page_setup.PageWidth
                - page_setup.LeftMargin
                - page_setup.RightMargin
            )

            # طول خط در حالت‌های چپ، راست و وسط: یک‌چهارم عرض متن
            line_width = text_width * 0.25
            remaining_width = text_width - line_width

            # دریافت خط جداکننده استاندارد Word
            separator = document.Footnotes.Separator

            # حذف جداکننده قبلی
            separator.Delete()

            paragraph = separator.ParagraphFormat

            # تعیین موقعیت خط
            if position == "چپ":
                paragraph.LeftIndent = 0
                paragraph.RightIndent = remaining_width

            elif position == "راست":
                paragraph.LeftIndent = remaining_width
                paragraph.RightIndent = 0

            elif position == "وسط":
                paragraph.LeftIndent = remaining_width / 2
                paragraph.RightIndent = remaining_width / 2

            elif position == "ممتد":
                paragraph.LeftIndent = 0
                paragraph.RightIndent = 0

            # ایجاد خط افقی در بالای پاراگراف جداکننده
            separator.Borders(-1).LineStyle = 1

        except Exception as error:
            messagebox.showerror(
                "تنظیم جداکننده پانویس",
                f"اعمال موقعیت جداکننده با مشکل مواجه شد:\n{error}",
            )
    
    
    def _apply_footnote_reference_style(self):
        """اعمال شیوه ارجاع روی تمام پانویس‌های سند."""

        try:
            self.engine.ensure_ready()

            document = self.engine.word.ActiveDocument

            reference_style = self.footnote_settings.get(
                "reference_style",
                "پیش‌فرض"
            )

            for index in range(1, document.Footnotes.Count + 1):
                footnote = document.Footnotes(index)

                reference_range = footnote.Reference.Duplicate
                reference_end = reference_range.End

                # بررسی کاراکتر بعد از شماره پانویس
                next_char = document.Range(
                    Start=reference_end,
                    End=reference_end + 1
                )

                if reference_style == "همراه با خط تیره":
                    if next_char.Text != "-":
                        reference_range.Collapse(0)
                        reference_range.InsertAfter("-")

                elif reference_style == "پیش‌فرض":
                    if next_char.Text == "-":
                        next_char.Delete()

        except Exception as error:
            messagebox.showerror(
                "تنظیم شیوه ارجاع پانویس",
                f"اعمال شیوه ارجاع با مشکل مواجه شد:\n{error}",
            )



