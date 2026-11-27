"""رابط انتخاب نشریه و ساخت مقاله بر اساس قالب آن."""

import re
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ..journals.manager import get_journals
from ..journals.template_builder import build_template
from ..article.wizard import create_article

def show_journal_selection(app):
    """فهرست نشریه‌ها را داخل محتوای پنجرهٔ اصلی نشان می‌دهد."""

    for widget in app.content.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        app.content,
        text="انتخاب نشریه برای ساخت مقاله",
        font=ctk.CTkFont(family="Vazirmatn", size=18, weight="bold"),
        text_color="#60A5FA",
    ).pack(anchor="e", padx=20, pady=(18, 6))

    try:
        journals = get_journals()
    except Exception as exc:
        messagebox.showerror("خطا در بارگذاری نشریه‌ها", str(exc), parent=app)
        return

    if not journals:
        ctk.CTkLabel(
            app.content,
            text="هیچ نشریه‌ای ثبت نشده است.",
            text_color=app.muted,
        ).pack(pady=30)
        return

    list_frame = ctk.CTkScrollableFrame(
        app.content, fg_color="transparent", corner_radius=10
    )
    list_frame.pack(fill="both", expand=True, padx=18, pady=(4, 14))

    for journal in journals:
        card = ctk.CTkFrame(
            list_frame,
            fg_color=app.panel_light,
            corner_radius=12,
            border_width=1,
            border_color=app.line,
        )
        card.pack(fill="x", padx=4, pady=6)

        ctk.CTkLabel(
            card,
            text=journal["name"],
            font=ctk.CTkFont(family="Vazirmatn", size=14, weight="bold"),
            text_color=app.text,
        ).pack(fill="x", padx=14, pady=10)

        ctk.CTkButton(
            card,
            text="ساخت مقاله با این نشریه",
            command=lambda item=journal: create_journal_article(app, item),
        ).pack(anchor="e", padx=12, pady=12)


def create_journal_article(app, journal):
    """اول فرم اطلاعات مقاله را نشان می‌دهد؛ با تأیید فرم، سند ساخته می‌شود."""
    from .article_form import show_article_form

    show_article_form(
        app, journal, on_submit=lambda form: build_article_document(app, journal, form)
    )

def safe_filename(text, fallback="Article", max_len=80):
    """عنوان مقاله را به اسم فایل مجاز ویندوز تبدیل می‌کند."""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", text)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:max_len].strip(" .") or fallback


def build_article_document(app, journal, form):
    """سند Word را از قالب نشریه می‌سازد و با اطلاعات فرم پر می‌کند."""

    safe_id = re.sub(
        r"[^A-Za-z0-9_-]+", "_", str(journal["id"])
    ).strip("_") or "journal"

    output_path = filedialog.asksaveasfilename(
        parent=app,
        title="ذخیره مقاله جدید",
        initialfile=f"{safe_filename(form['title_fa'], f'Article_{safe_id}')}.docx",
        defaultextension=".docx",
        filetypes=[("Word Document", "*.docx")],
    )
    if not output_path:
        return

    try:
        template_dir = Path.home() / "Documents" / "PythonNegar" / "Templates"
        template_dir.mkdir(parents=True, exist_ok=True)
        template_path = template_dir / f"{safe_id}.dotx"

        build_template(journal, template_path)

        doc_name = create_article(app.engine, form, output_path, template_path)

        app.update_status(
            "مقاله ساخته و پر شد.",
            is_connected=True,
            doc_name=doc_name,
        )
        messagebox.showinfo(
            "ساخت سند",
            f"سند مقاله با قالب «{journal['name']}» ساخته و پر شد.",
            parent=app,
        )
    except Exception as exc:
        messagebox.showerror(
            "خطا در ساخت مقاله",
            f"ساخت مقاله انجام نشد:\n{exc}",
            parent=app,
        )