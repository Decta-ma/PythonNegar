from ..registry import card, placeholder
from ..ui_components.journal_selection import show_journal_selection

TAB = "مقاله‌نگار"

placeholder(TAB, "قالب پایان‌نامه", "تنظیم ساختار پایان‌نامه", order=10)


@card(TAB, "قالب مقاله", "تنظیم ساختار مقاله", order=20)
def article_template(app):
    show_journal_selection(app)


placeholder(TAB, "قالب گزارش", "تنظیم ساختار گزارش", order=30)