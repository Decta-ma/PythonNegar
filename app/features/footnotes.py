from ..registry import card, placeholder
from ..ui_components.footnote_settings import show_footnote_settings_modal

TAB = "پانویس"


@card(
    TAB,
    "درج پانویس(پاورقی)",
    "افزودن پانویس به سند",
    order=10,
    anchor=True,
    settings=show_footnote_settings_modal,
)
def insert_footnote(app, anchor):
    app.footnote_menu_action(anchor)


placeholder(TAB, "مدیریت پانویس‌ها", "مشاهده و تنظیم پانویس‌ها", order=20)
placeholder(TAB, "قالب پانویس", "تنظیم قلم و فاصله", order=30)