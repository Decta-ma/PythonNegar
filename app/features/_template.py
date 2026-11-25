from ..registry import card, placeholder

TAB = "مدیریت متن"  # یکی از registry.TAB_NAMES

# کارت غیرفعال:
# placeholder(TAB, "نام کارت", "توضیح", order=40)

# کارت فعال:
# @card(TAB, "نام کارت", "توضیح", order=40)
# def my_feature(app):
#     from ..ui_components.my_dialog import show_my_dialog
#     show_my_dialog(app)

# منوی کشویی زیر کارت: anchor=True  => fn(app, anchor_widget)
# دکمهٔ تنظیمات ↖:       settings=show_x  => fn(app)