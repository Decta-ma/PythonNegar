"""اکشن‌های مربوط به مدیریت سند (Mixin رابط کاربری)."""

from tkinter import filedialog, messagebox

import customtkinter as ctk


class DocumentActions:
    """اکشن‌های سند؛ به‌صورت Mixin به‌همراه ctk.CTk استفاده می‌شود."""

    # ------------------------------------------------------------ اکشن‌ها
    def create_doc_action(self):
        try:
            path = filedialog.asksaveasfilename(
                parent=self,
                title="ذخیره سند جدید با امضای نرم‌افزار",
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx")],
            )
            if path:
                doc_name = self.engine.create_new_signed_doc(path)
                self.update_status("سند ایجاد و متصل شد", is_connected=True, doc_name=doc_name)
                messagebox.showinfo("موفقیت", f"سند «{doc_name}» با موفقیت ایجاد و امضا شد.")
        except Exception as e:
            self.update_status("وضعیت: سندی متصل نیست", is_connected=False)
            messagebox.showerror("خطا", str(e), parent=self)

    def connect_doc_action(self):
        try:
            doc_name = self.engine.connect_to_active()
            self.update_status("اتصال به سند برقرار شد", is_connected=True, doc_name=doc_name)
            messagebox.showinfo("تأیید امضا", f"امضای سند «{doc_name}» با موفقیت تأیید شد.")
        except Exception as e:
            self.update_status("وضعیت: سندی متصل نیست", is_connected=False)
            messagebox.showerror("خطای اتصال و لایسنس", str(e), parent=self)

    def rename_doc_action(self):
        try:
            current_doc = self.engine.ensure_ready()
            current_name = current_doc.Name

            # باز کردن دیالوگ دریافت نام جدید
            dialog = ctk.CTkInputDialog(
                text=f"نام فعلی: {current_name}\n\nنام جدید سند را وارد کنید:",
                title="تغییر نام رسمی سند",
            )
            new_name = dialog.get_input()

            if new_name and new_name.strip():
                updated_name = self.engine.rename_active_document(new_name.strip())
                self.update_status("نام سند به‌روزرسانی شد", is_connected=True, doc_name=updated_name)
                messagebox.showinfo(
                    "موفقیت",
                    f"نام فایل به «{updated_name}» تغییر کرد و کلید امنیتی با موفقیت به‌روزرسانی شد.",
                    parent=self,
                )
        except Exception as e:
            self.update_status("وضعیت: سندی متصل نیست", is_connected=False)
            messagebox.showerror("خطا در تغییر نام", str(e), parent=self)

    def fix_spaces_action(self):
        try:
            msg = self.engine.fix_extra_spaces()
            self.update_status(msg)
            messagebox.showinfo("نتیجه", msg, parent=self)
        except Exception as e:
            self.update_status("خطا در پاکسازی فاصله‌ها", is_connected=False)
            messagebox.showerror("خطا", str(e), parent=self)

    def make_red_action(self):
        try:
            msg = self.engine.set_selection_red()
            self.update_status(msg)
            messagebox.showinfo("نتیجه", msg, parent=self)
        except Exception as e:
            self.update_status("خطا در تغییر رنگ متن", is_connected=False)
            messagebox.showerror("خطا", str(e), parent=self)
