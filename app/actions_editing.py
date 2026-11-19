"""اکشن‌های کارت «ویراستاری» (Mixin رابط کاربری)."""

from tkinter import messagebox

import customtkinter as ctk

try:  # اجرا به‌صورت پکیج
    from .glass_dropdown import GlassDropdown
    from .data_loader import load_group
    from .replace_engine import apply_rules
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    from app.glass_dropdown import GlassDropdown
    from app.data_loader import load_group
    from app.replace_engine import apply_rules

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

    # ------------------------------------------------------------ قواعد CSV
    def half_space_action(self):
        self._run_rule_group("half_space", "نیم‌فاصله‌گذاری")

    def punctuation_action(self):
        self._run_rule_group("punctuation", "نشانه‌گذاری (سجاوندی)")

    def spelling_action(self):
        self._run_rule_group("spelling", "اصلاح غلط‌های املایی")

    def standard_language_action(self):
        self._run_rule_group("standard", "زبان معیار")

    def _run_rule_group(self, group, title):
        """قواعد یک گروه CSV را روی سند متصل اعمال می‌کند (الگوی مشترک آیتم‌ها)."""
        if getattr(self, "_rules_running", False):
            return
        self._rules_running = True
        try:
            ruleset = load_group(group)

            def progress(done, total):
                if done % 3 == 0 or done == total:
                    self.update_status(f"{title}… {done} از {total}")
                    self.update_idletasks()

            report = apply_rules(self.engine, ruleset.rules, undo_name=title, progress=progress)
            self._restore_connected_status()
            messagebox.showinfo(title, report.message(title), parent=self)
        except Exception as e:
            self._restore_connected_status()
            messagebox.showerror("خطا", str(e), parent=self)
        finally:
            self._rules_running = False

    def _restore_connected_status(self):
        """بازگرداندن نوار وضعیت به «متصل به ...» (بدون قطع اتصال در خطای عملیات متنی)."""
        try:
            self.update_status("", is_connected=True, doc_name=self.engine.doc.Name)
        except Exception:
            pass