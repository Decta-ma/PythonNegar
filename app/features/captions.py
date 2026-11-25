from ..registry import card, placeholder

TAB = "عنوان و ارجاع"

placeholder(TAB, "عنوان‌ها", "درج و قالب‌بندی عنوان‌ها", order=10)


@card(TAB, "جدول عدد", "شماره‌گذاری جدول‌ها", order=20)
def table_number(app):
    app.insert_table_number()


@card(TAB, "عنوان شکل", "عنوان‌گذاری و شماره‌گذاری", order=30)
def figure_caption(app):
    app.insert_figure_caption()


@card(TAB, "معادله نویسی", "درج و ویرایش معادلات ریاضی", order=40)
def equation(app):
    app.equation_action()
    