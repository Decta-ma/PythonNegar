"""اکشن‌های کارت «ویراستاری» (Mixin رابط کاربری)."""

from tkinter import messagebox

import customtkinter as ctk

try:  # اجرا به‌صورت پکیج
    from .glass_dropdown import GlassDropdown
    from .data_loader import load_group
    from .replace_engine import apply_rules
    from .poetry_formatter import (
    format_poetry_single_column,
    format_poetry_two_columns,
   )
    from .number_converter import (
    convert_document_to_persian,
    convert_document_to_english,
  )  
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    from app.glass_dropdown import GlassDropdown
    from app.data_loader import load_group
    from app.replace_engine import apply_rules
    from app.poetry_formatter import (
    format_poetry_single_column,
    format_poetry_two_columns,
   )
    from app.number_converter import (
    convert_document_to_persian,
    convert_document_to_english,
   )

# ساختار منو: (عنوان, [زیرآیتم‌ها] یا None)
EDITING_MENU = [
    ("ویراستاری مقدماتی", ["نیم فاصله گذاری", "نشانه گذاری (سجاوندی)", "غلط املایی","زبان معیار"]),
    ("تبدیل اعداد", ["به فارسی", "به انگلیسی"]),
    ("قالب شعر", ["تک ستونه", "دو ستونه"]),
]

# نگاشت «مسیر آیتم» به «نام متد اکشن». هر قابلیت که پیاده شد، اینجا اضافه می‌شود.
EDITING_HANDLERS = {
    ("ویراستاری مقدماتی", "نیم فاصله گذاری"): "half_space_action",
    ("ویراستاری مقدماتی", "نشانه گذاری (سجاوندی)"): "punctuation_action",
    ("ویراستاری مقدماتی", "غلط املایی"): "spelling_action",
    ("ویراستاری مقدماتی","زبان معیار",): "standard_language_action",
    ("قالب شعر", "تک ستونه"): "poetry_single_column_action",
    ("قالب شعر", "دو ستونه"): "poetry_two_columns_action",
    ("تبدیل اعداد", "به فارسی"): "convert_numbers_to_persian_action",
    ("تبدیل اعداد", "به انگلیسی"): "convert_numbers_to_english_action",
}


def _norm(text):
    """یکسان‌سازی نیم‌فاصله/فاصله و ی-ک عربی تا تفاوت نویسه‌ها مانع تطبیق نشود."""
    text = text.replace("\u200c", " ").replace("ي", "ی").replace("ك", "ک")
    return " ".join(text.split())


def _norm_path(path):
    return tuple(_norm(part) for part in path)


def _find_handler(path):
    wanted = _norm_path(path)
    for key, method_name in EDITING_HANDLERS.items():
        if _norm_path(key) == wanted:
            return method_name
    return None


class EditingActions:
    """اکشن‌های ویراستاری؛ به‌صورت Mixin به‌همراه ctk.CTk استفاده می‌شود."""

    def editing_menu_action(self, card):
        """باز/بستن منوی شیشه‌ای زیر کارت «ویراستاری»."""
        try:
            popup = getattr(self, "_editing_popup", None)
            if popup is not None and popup.is_open:
                popup.close()
                return

            try:
                scale = ctk.ScalingTracker.get_window_scaling(self)
            except Exception:
                scale = 1.0

            self._editing_popup = GlassDropdown(
                self, card, EDITING_MENU,
                on_select=self._on_editing_select, scale=scale,
            )
            self._editing_popup.open()
        except Exception as e:
            messagebox.showerror("خطا", str(e), parent=self)

    def _on_editing_select(self, path):
        """path یک تاپل است، مثل ('تبدیل اعداد', 'به فارسی') یا ('زبان معیار',)."""
        handler_name = _find_handler(path)
        if handler_name:
            getattr(self, handler_name)()
            return
        messagebox.showinfo(
            "ویراستاری",
            "«" + " ← ".join(path) + "»\nاین قابلیت هنوز پیاده‌سازی نشده است.",
            parent=self,
        )
        
        # ------------------------------------------------------------
    # مدیریت محدوده اعمال عملیات ویراستاری

    def _get_editing_range(self):
        """
        مشخص می‌کند عملیات ویراستاری روی انتخاب کاربر انجام شود
        یا روی کل سند.

        خروجی:
            (doc, target_range)
        """

        doc = self.engine.ensure_ready()
        selection = self.engine.word.Selection
        selected_range = selection.Range.Duplicate

        # اگر کاربر متنی انتخاب کرده باشد
        if selected_range.Start != selected_range.End:
            return doc, selected_range

        # اگر انتخابی وجود نداشته باشد
        apply_to_document = messagebox.askyesno(
            "اعمال تغییرات",
            "شما هیچ موردی را برای تغییر انتخاب نکرده‌اید، "
            "آیا می‌خواهید این تغییر روی کل سند اعمال شود؟",
            parent=self,
        )

        if not apply_to_document:
            return None, None

        # کل محتوای اصلی سند
        return doc, doc.Content.Duplicate

    # ------------------------------------------------------------ قواعد CSV
    def half_space_action(self):
        """اجرای اصلاح نیم‌فاصله روی متن اصلی و بخش‌های انتخاب‌شده."""

        include_footnotes = self._is_editing_option_enabled(
            "footnotes"
        )

        include_headers_footers = self._is_editing_option_enabled(
            "headers_footers"
        )

        self._run_rule_group(
            "half_space",
            "نیم‌فاصله‌گذاری",
            include_footnotes=include_footnotes,
            include_headers_footers=include_headers_footers,
        )

    def punctuation_action(self):
        self._run_rule_group("punctuation", "نشانه‌گذاری (سجاوندی)")

    def spelling_action(self):
        self._run_rule_group("spelling", "اصلاح غلط‌های املایی")

    def standard_language_action(self):
        self._run_rule_group("standard", "زبان معیار")
    
        # ------------------------------------------------------------
    # تبدیل اعداد

    def convert_numbers_to_persian_action(self):
        self._run_number_conversion(
            convert_document_to_persian,
            "تبدیل اعداد به فارسی",
        )

    def convert_numbers_to_english_action(self):
        self._run_number_conversion(
            convert_document_to_english,
            "تبدیل اعداد به انگلیسی",
        )

    def _run_number_conversion(self, converter, title):
        """اجرای تبدیل اعداد روی انتخاب کاربر یا کل سند."""

        try:
            self.update_status(f"{title}...")

            doc, target_range = self._get_editing_range()

            # کاربر گزینه «خیر» را انتخاب کرده است.
            if doc is None:
                self._restore_connected_status()
                return

            changed_count = converter(
                doc,
                target_range,
            )

            doc.Save()

            self._restore_connected_status()

            messagebox.showinfo(
                title,
                f"عملیات با موفقیت انجام شد.\n"
                f"تعداد اعداد تبدیل‌شده: {changed_count}",
                parent=self,
            )

        except Exception as e:
            self._restore_connected_status()

            messagebox.showerror(
                "خطا در تبدیل اعداد",
                str(e),
                parent=self,
            )
            
    def _run_rule_group(
        self,
        group,
        title,
        include_footnotes=False,
        include_headers_footers=False,
    ):
        """اجرای قواعد CSV روی انتخاب کاربر یا کل سند."""

        if getattr(self, "_rules_running", False):
            return

        self._rules_running = True

        try:
            doc, target_range = self._get_editing_range()

            # کاربر «خیر» را انتخاب کرده است.
            if doc is None:
                self._restore_connected_status()
                return
            
                        # محدوده‌های اضافی که باید در کنار متن اصلی بررسی شوند.
            extra_ranges = []

            # --------------------------------------------------------
            # پانویس‌ها
            # --------------------------------------------------------

            if include_footnotes:
                try:
                    for index in range(1, doc.Footnotes.Count + 1):
                        footnote = doc.Footnotes(index)
                        extra_ranges.append(
                            footnote.Range.Duplicate
                        )
                except Exception:
                    pass

            # --------------------------------------------------------
            # سرصفحه و پاصفحه
            # --------------------------------------------------------

            if include_headers_footers:
                try:
                    for section_index in range(
                        1,
                        doc.Sections.Count + 1,
                    ):
                        section = doc.Sections(section_index)

                        # 1 = اول
                        # 2 = زوج
                        # 3 = فرد
                        for story_type in (1, 2, 3):
                            try:
                                header = section.Headers(story_type)

                                if header.Exists:
                                    extra_ranges.append(
                                        header.Range.Duplicate
                                    )
                            except Exception:
                                pass

                            try:
                                footer = section.Footers(story_type)

                                if footer.Exists:
                                    extra_ranges.append(
                                        footer.Range.Duplicate
                                    )
                            except Exception:
                                pass
                except Exception:
                    pass

            ruleset = load_group(group)

            def progress(done, total):
                if done % 3 == 0 or done == total:
                    self.update_status(
                        f"{title}… {done} از {total}"
                    )
                    self.update_idletasks()

            report = apply_rules(
                self.engine,
                ruleset.rules,
                undo_name=title,
                progress=progress,
                target_range=target_range,
                target_ranges=extra_ranges,
            )

            self._restore_connected_status()

            messagebox.showinfo(
                title,
                report.message(title),
                parent=self,
            )

        except Exception as e:
            self._restore_connected_status()

            messagebox.showerror(
                "خطا",
                str(e),
                parent=self,
            )

        finally:
            self._rules_running = False

    def _restore_connected_status(self):
        """بازگرداندن نوار وضعیت به «متصل به ...» (بدون قطع اتصال در خطای عملیات متنی)."""
        try:
            self.update_status("", is_connected=True, doc_name=self.engine.doc.Name)
        except Exception:
            pass
        
    

    def poetry_single_column_action(self):
        self._run_poetry_action(
            format_poetry_single_column,
            "قالب شعر - تک ستونه",
        )

    def poetry_two_columns_action(self):
        self._run_poetry_action(
            format_poetry_two_columns,
            "قالب شعر - دو ستونه",
        )

   
    def _run_poetry_action(self, formatter, title):
        """اجرای قالب‌بندی شعر روی انتخاب کاربر یا کل سند."""

        try:
            self.update_status(f"{title}...")

            doc, target_range = self._get_editing_range()

            # کاربر گزینه «خیر» را انتخاب کرده است.
            if doc is None:
                self._restore_connected_status()
                return

            result = formatter(
                self.engine,
                target_range,
            )

            self._restore_connected_status()

            messagebox.showinfo(
                title,
                result,
                parent=self,
            )

        except Exception as e:
            self._restore_connected_status()

            messagebox.showerror(
                "خطا در قالب‌بندی شعر",
                str(e),
                parent=self,
            )
    
    def _is_editing_option_enabled(self, key):
        """بررسی فعال بودن یک گزینه از تنظیمات ویراستاری."""

        controls = getattr(self, "editing_settings_controls", {})

        control = controls.get(key)

        if control is None:
            return False

        try:
            return bool(control.get())
        except Exception:
            return False

