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

        # نگهداری زبان انتخاب‌شده برای استفاده هنگام درج پانویس
        self.footnote_language = language

        # تنظیمات پیش‌فرض در صورت نبود تنظیمات ذخیره‌شده
        if not hasattr(self, "footnote_settings"):
            self.footnote_settings = {
                "auto_keyboard": True,
                "auto_direction": True,
                "default_language": "فارسی",
            }

        # تغییر زبان کیبورد در صورت فعال بودن تنظیم مربوطه
        if self.footnote_settings.get("auto_keyboard", True):
            self._switch_footnote_keyboard(language)

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
                0x00000001,  # KLF_ACTIVATE
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
        """اعمال جهت نوشتار متناسب با زبان انتخاب‌شده روی پاراگراف پانویس."""
        if hasattr(self, "footnote_settings"):
         if not self.footnote_settings.get("auto_direction", True):
          return

        language = getattr(self, "footnote_language", "فارسی")

        # ثابت‌های Word:
        # 1 = راست به چپ
        # 0 = چپ به راست
        reading_order = 1 if language == "فارسی" else 0

        paragraph.Range.ParagraphFormat.ReadingOrder = reading_order
