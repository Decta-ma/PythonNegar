"""Config (data only) for JOSTARNAMEH (جستارنامه ادبیات تطبیقی).

Values measured from the original JOSTARNAMEH.dotm: A4, 2 cm margins, RTL,
Times New Roman (latin) + B Nazanin (complex), no header text.
"""

from ._parts import field, hint

JOSTARNAMEH = {
    "id": "JOSTARNAMEH",
    "name": "جستارنامه ادبیات تطبیقی",
    "short_name": "جستارنامه",

    "page": {
        "width_cm": 21.0, "height_cm": 29.7,
        "margin_top": 2.0, "margin_right": 2.0,
        "margin_bottom": 2.0, "margin_left": 2.0,
        "header_distance": 1.0, "footer_distance": 1.0,
        "rtl": True,
        "different_first_page": False,
        "even_odd_headers": False,
    },

    "fonts": {"latin": "Times New Roman", "complex": "B Nazanin", "base_size": 13},

    "header": {"line1": "", "line2": "", "size": 10, "border": False},

    "skeleton": [
        ("TitleNegar", hint("TitleFa", "عنوان فارسی مقاله", "عنوان مقاله")),
        ("TitleNegarAuthor", {"text": "نام نویسندگان", "bookmark": "AuthorNamesFa"}),

        ("AbstractHeadNegar", "چکیده"),
        ("AbstractBodyNegar", "متن چکیده را اینجا بنویسید."),
        ("KeywordsNegar", [{"text": "واژه‌های کلیدی: ", "bold": True},
                           hint("KeywordsFa", "واژه‌های کلیدی",
                                "کلیدواژه‌ها را با ویرگول از هم جدا کنید.")]),

        ("TitleNegar1", "مقدمه"),
        ("BodyNegar", hint("G_JOSTARNAMEH_Guide_Introduction", "راهنمای مقدمه",
                           "شامل: بیان مسأله، اهمیت و ضرورت، پیشینۀ تحقیق و روش کار.")),

        ("TitleNegar1", "بحث"),
        ("BodyNegar", hint("G_JOSTARNAMEH_Guide_Discussion", "راهنمای بحث",
                           "تحلیل و بررسی مباحث و داده‌ها.")),

        ("TitleNegar1", "نتیجۀ بحث"),
        ("BodyNegar", hint("G_JOSTARNAMEH_Guide_DiscussionResult", "راهنمای نتیجه",
                           "نتیجه‌گیری از مباحث را بنویسید.")),

        ("TitleNegar1", "فهرست منابع و مآخذ"),
        ("RefNegar", hint("G_JOSTARNAMEH_Guide_References", "راهنمای منابع",
                          "منابع فارسی و سپس منابع خارجی (به تفکیک کتاب، مقاله، منابع الکترونیکی و...) "
                          "را براساس نام خانوادگی مؤلفان به‌صورت الفبایی بنویسید؛ همۀ منابع به زبان "
                          "لاتین ترجمه و پس از منابع فارسی درج شوند.")),

        # English abstract: new page, left-to-right
        ("TitleNegar", hint("TitleEn", "English title", "Article Title"),
         {"rtl": False, "page_break": True, "before": 0}),
        ("TitleNegarAuthor", {"text": "Author Names", "bookmark": "AuthorNamesEn"}, {"rtl": False}),
        ("AbstractHeadNegar", "Abstract", {"rtl": False, "align": "left"}),
        ("AbstractBodyNegar", "Type the abstract here.", {"rtl": False, "align": "both"}),
        ("KeywordsNegar", [{"text": "Keywords: ", "bold": True},
                           hint("KeywordsEn", "English keywords",
                                "Separate keywords with commas.")],
         {"rtl": False, "align": "left"}),
    ],

    "styles": {
        "BaseNegar": {"size": 13, "after": 0, "line": 1.0},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor",
                       "size": 16, "bold": True, "align": "center",
                       "before": 12, "after": 12, "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar",
                        "size": 14, "bold": True, "before": 12, "after": 6,
                        "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar",
                        "size": 13, "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar",
                        "size": 13, "outline": 2},
        "TitleNegarAuthor": {"based_on": "BaseNegar", "size": 12,
                             "align": "center", "after": 12},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "size": 12, "bold": True, "before": 6, "after": 3,
                              "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "size": 12,
                              "align": "both", "after": 6},
        "KeywordsNegar": {"based_on": "BaseNegar", "size": 11,
                          "align": "both", "after": 12},
        "BodyNegar": {"based_on": "BaseNegar", "next": "BodyNegar", "size": 13,
                      "align": "both", "after": 6, "first_line_cm": 0.5},
        "TableCaptionNegar": {"based_on": "BaseNegar", "size": 11, "bold": True,
                              "align": "center", "before": 12, "after": 6,
                              "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "size": 11, "bold": True,
                               "align": "center", "after": 12},
        "TableTextNegar": {"based_on": "BaseNegar", "size": 11, "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "next": "RefNegar", "size": 12,
                     "align": "both", "after": 4, "left_cm": 0.5, "hanging_cm": 0.5},
        "FootnoteTextFa": {"based_on": "BaseNegar", "size": 10, "align": "right"},
        "FootnoteTextEn": {"based_on": "BaseNegar", "size": 10, "align": "left"},
    },
}

JOURNAL = JOSTARNAMEH