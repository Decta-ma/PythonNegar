"""Config (data only) for TCAT - رویکرد الهی ـ فرهنگی در تدریس (Persian, RTL).

Values read from TCAT.dotm: A4 (11907x16840 twips), top 2.5 cm, sides and bottom 2.0 cm,
complex font B Mitra 11 pt, titles B Compset 20 pt / B Nazanin 14 pt (estimates from styles.xml).
Header text is taken from header2.xml (running journal line).
"""

from ._parts import field, hint

TCAT = {
    "id": "TCAT",
    "name": "رویکرد الهی ـ فرهنگی در تدریس",
    "short_name": "TCAT",

    "page": {
        "width_cm": 21.0, "height_cm": 29.7,
        "margin_top": 2.5, "margin_right": 2.0,
        "margin_bottom": 2.0, "margin_left": 2.0,
        "header_distance": 1.27, "footer_distance": 1.27,
        "rtl": True,
        "different_first_page": False,
        "even_odd_headers": False,
    },

    "fonts": {"latin": "Times New Roman", "complex": "B Mitra", "base_size": 11},

    "header": {
        "line1": "دوره ۱، شماره ۱، پاییز ۱۴۰۴، صفحات",
        "line2": "",
        "size": 9, "border": False,
    },

    "skeleton": [
        ("TitleNegar", hint("TitleFa", "عنوان مقاله", "عنوان مقاله")),
        ("TitleNegarAuthor", {"text": "نام نویسندگان", "bookmark": "AuthorNamesFa"}),

        ("AbstractHeadNegar", "اطلاعات مقاله"),
        ("KeywordsNegar", [{"text": "نوع مقاله: ", "bold": True},
                           hint("ArticleType", "نوع مقاله", "پژوهشی")]),
        ("KeywordsNegar", [{"text": "تاریخچه مقاله: ", "bold": True}]),
        ("KeywordsNegar", [{"text": "تاریخ دریافت: ", "bold": True},
                           field("JournalReceivedDate", "تاریخ دریافت", "//")]),
        ("KeywordsNegar", [{"text": "تاریخ بازنگری: ", "bold": True},
                           field("JournalRevisedDate", "تاریخ بازنگری", "//")]),
        ("KeywordsNegar", [{"text": "تاریخ پذیرش: ", "bold": True},
                           field("JournalAcceptedDate", "تاریخ پذیرش", "//")]),
        ("KeywordsNegar", [{"text": "نویسنده مسئول: ", "bold": True}]),
        ("KeywordsNegar", [{"text": "DOI: ", "bold": True}]),

        ("AbstractHeadNegar", "چکیده"),
        ("AbstractBodyNegar", hint("AbstractFa", "متن چکیده",
                                   "متن چکیده را اینجا بنویسید.", block=True)),
        ("KeywordsNegar", [{"text": "کلیدواژه‌ها: ", "bold": True},
                           hint("KeywordsFa", "کلیدواژه‌ها",
                                "کلیدواژه‌ها را با ویرگول از هم جدا کنید.")]),

        ("TitleNegar1", "1. مقدمه"),
        ("BodyNegar", hint("G_TCAT_Guide_Introduction", "راهنمای مقدمه",
                           "بیان مسئله، ضرورت و اهمیت، پیشینه و هدف پژوهش را بنویسید.")),
        ("TitleNegar1", "2. روش‌شناسی پژوهش"),
        ("BodyNegar", hint("G_TCAT_Guide_Methodology", "راهنمای روش‌شناسی",
                           "نوع پژوهش، جامعه و نمونه، ابزار گردآوری داده، روایی و پایایی و روش تحلیل داده‌ها را شرح دهید.")),
        ("TitleNegar1", "3. یافته‌های پژوهش"),
        ("BodyNegar", hint("G_TCAT_Guide_Findings", "راهنمای یافته‌ها",
                           "توضیحات متنی یافته‌ها را همراه با ارجاع به جدول‌ها و شکل‌ها بنویسید.")),
        ("TitleNegar1", "4. بحث و نتیجه‌گیری"),
        ("BodyNegar", hint("G_TCAT_Guide_Discussion", "راهنمای بحث",
                           "یافته‌ها را با پژوهش‌های پیشین مقایسه کنید و نتیجه‌گیری و پیشنهادها را بنویسید.")),
        ("TitleNegar1", "منابع"),
        ("RefNegar", hint("G_TCAT_Guide_References", "راهنمای منابع",
                          "منابع فارسی و سپس لاتین را به ترتیب الفبا بنویسید. ارجاع درون‌متنی به‌صورت (نام‌خانوادگی، سال) باشد.")),
        ("TitleNegar1", "تقدیر و تشکر"),
        ("RefNegar", hint("G_TCAT_Guide_Acknowledgement", "راهنمای تقدیر",
                          "در صورت لزوم از افراد یا نهادهای حامی پژوهش تقدیر کنید؛ اگر موردی ندارید، این بخش را حذف کنید.")),
    ],

    "styles": {
        "BaseNegar": {"font": "B Mitra", "size": 11},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor", "size": 20,
                       "bold": True, "align": "center", "before": 6, "after": 6, "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar", "size": 14, "bold": True,
                        "align": "both", "before": 6, "after": 2, "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar", "size": 12,
                        "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar", "size": 11,
                        "outline": 2},
        "TitleNegarAuthor": {"based_on": "BaseNegar", "size": 12, "bold": True,
                             "align": "center", "before": 6, "after": 6},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "size": 12, "bold": True, "align": "center", "line": 0.8,
                              "color": "222A35", "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "size": 10, "align": "both"},
        "KeywordsNegar": {"based_on": "BaseNegar", "size": 10, "line": 1.3,
                          "align": "both"},
        "BodyNegar": {"based_on": "BaseNegar", "next": "BodyNegar", "size": 11,
                      "align": "both", "before": 6, "after": 2, "first_line_cm": 0.5},
        "TableCaptionNegar": {"based_on": "BaseNegar", "size": 10, "bold": True,
                              "align": "center", "before": 6, "after": 2, "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "size": 10, "bold": True,
                               "align": "center", "before": 2, "after": 6},
        "TableTextNegar": {"based_on": "BaseNegar", "size": 10, "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "next": "RefNegar", "size": 10,
                     "align": "both", "before": 2, "after": 2,
                     "left_cm": 1.0, "hanging_cm": 1.0},
        "FootnoteText": {"based_on": "BaseNegar", "size": 9, "align": "right"},
    },
}

JOURNAL = TCAT