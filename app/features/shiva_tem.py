from ..registry import card, placeholder
from ..ui_components.journal_selection import show_journal_selection


TAB="شیوانگار"

@card(TAB, "ساخت مقاله جدید", "تنظیم ساختار شیوانگار", order=20)
def article_template(app):
    show_journal_selection(app)

placeholder(TAB, "مقاله‌های جاری", "مقاله‌های ثبت‌شده روی سرور", order=21)
placeholder(TAB, "مقاله‌های بایگانی", "مقاله‌های بایگانی‌شده روی سرور", order=22)
placeholder(TAB, "قالب گزارش", "تنظیم ساختار گزارش", order=30)