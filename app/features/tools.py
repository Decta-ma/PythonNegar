from ..registry import card, placeholder
from ..ui_components.about_program import show_about_program_menu
from ..ui_components.help_menu import show_help_menu

TAB = "ابزارها"

placeholder(TAB, "تنظیمات", "تنظیمات برنامه", order=10)


@card(TAB, "راهنما", "راهنمای استفاده", order=20, anchor=True)
def help_menu(app, anchor):
    show_help_menu(app, anchor)


@card(TAB, "دربارهٔ برنامه", "اطلاعات نسخه", order=30, anchor=True)
def about(app, anchor):
    show_about_program_menu(app, anchor)