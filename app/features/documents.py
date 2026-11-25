from ..registry import card, placeholder
from ..ui_components.editing_settings import show_editing_settings_modal

TAB = "مدیریت سند"


@card(TAB, "ساخت سند جدید", "ایجاد سند دانشگاهی", order=10)
def create_doc(app):
    app.create_doc_action()


@card(TAB, "اتصال به سند باز", "اتصال به سند فعال Word", order=20)
def connect_doc(app):
    app.connect_doc_action()


@card(TAB, "تغییر نام سند", "تغییر نام از داخل برنامه", order=30)
def rename_doc(app):
    app.rename_doc_action()


placeholder(TAB, "وضعیت سند", "نمایش اطلاعات و وضعیت سند", order=40)
placeholder(TAB, "ذخیرهٔ نسخه", "مدیریت نسخه‌های سند", order=50)


@card(
    TAB,
    "ویراستاری",
    "ویرایش سند",
    order=60,
    anchor=True,
    settings=show_editing_settings_modal,
)
def editing(app, anchor):
    app.editing_menu_action(anchor)
    