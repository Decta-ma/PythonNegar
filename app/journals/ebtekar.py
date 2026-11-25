"""Config (data only) for the Ebtekar journal template.

Change a number here, build again, and the .dotm changes.
Units: margins in cm, font sizes in pt, spacing in pt, indents in cm.
"""

from ._parts import field, hint

EBTEKAR = {
    "id": "Ebtekar",
    "name": "نشریه علمی ابتکار و خلاقیت در علوم انسانی",
    "short_name": "ابتکار و خلاقیت در علوم انسانی",

    # ---- page ----
    "page": {
        "width_cm": 21.0, "height_cm": 29.7,          # A4
        "margin_top": 4.5, "margin_right": 4.9,
        "margin_bottom": 2.5, "margin_left": 2.5,
        "header_distance": 1.25, "footer_distance": 1.25,
        "rtl": True,
        "different_first_page": True,
        "even_odd_headers": True,
    },

    # ---- default fonts ----
    "fonts": {
        "latin": "Times New Roman",
        "complex": "B Zar",          # Persian font
        "base_size": 12,
    },

    # ---- header (odd pages) ----
    "header": {
        "line1": "نشریه علمی ابتکار و خلاقیت در علوم انسانی",
        "line2": "دورهٔ … ، شمارهٔ … ، فصل … سال …",
        "size": 10,
        "border": True,
    },


    # ---- starting content of a new article (same order as Journals.xml) ----
    # Each item is (style id, parts, options). parts = text, a field/hint, or a list of them.
    "skeleton": [
        # 1_TitleAndauthorss: journal info table, then title and authorss
        {"table": {
            "widths_cm": [0.45, 11.93],
            "cells": [
                [],
                [
                    ("Header", [{"text": "نشریه علمی "},
                                {"text": "ابتکار و خلاقیت در علوم انسانی",
                                 "bold": True, "italic": True}]),
                    ("Header", ["دورة ", field("JournalVolume", "Volume"),
                                " ، شمارة ", field("JournalIssue", "Issue"),
                                " ، ", field("JournalSeason", "Season"), " ",
                                field("JournalYear", "Year"),
                                "، صص. مقاله پژوهشی"]),
                    ("Header", ["تاریخ دریافت: ",
                                field("JournalReceivedDate", "Received date", "//")],
                     {"border_top": True, "before": 6}),
                    ("Header", ["تاریخ پذیرش: ",
                                field("JournalAcceptedDate", "Accepted date", "//")]),
                ],
            ],
        }},
        ("BodyNegar", ""),
        ("TitleNegar", hint("TitleFa", "عنوان فارسی مقاله", "عنوان مقاله")),
        ("TitleNegarauthors", {"text": "نام نویسندگان", "bookmark": "authorsNamesFa"}),

        # 2_Abstract
        ("AbstractHeadNegar", "چکیده"),
        ("AbstractBodyNegar", hint("AbstractFa", "چکیده فارسی",
                                   "متن چکیده را اینجا بنویسید.", block=True)),
        ("KeywordsNegar", [{"text": "واژه‌های کلیدی: ", "bold": True},
                           hint("KeywordsFa", "واژه‌های کلیدی",
                                "کلیدواژه‌ها را با ویرگول از هم جدا کنید.")]),

        # 3 to 9: heading + guide text
        ("TitleNegar1", "مقدمه"),
        ("BodyNegar", hint("G_Ebtekar_Guide_Introduction", "راهنمای مقدمه",
            "مقدمه: بیان مسئله، ضرورت و اهمیت پژوهش و هدف یا پرسش‌های اصلی مقاله را بنویسید.")),
        ("TitleNegar1", "مبانی نظری و توسعه فرضیه‌ها"),
        ("BodyNegar", hint("G_Ebtekar_Guide_TheoreticalBackground", "راهنمای مبانی نظری",
            "مبانی نظری، پیشینهٔ پژوهش و منطق توسعهٔ فرضیه‌ها را به‌صورت دسته‌بندی‌شده و با ارجاع به منابع ارائه کنید.")),
        ("TitleNegar1", "روش‌شناسی پژوهش"),
        ("BodyNegar", hint("G_Ebtekar_Guide_Methodology", "راهنمای روش‌شناسی",
            "نوع پژوهش، جامعه و نمونه، ابزار گردآوری داده و روایی و پایایی آن، و روش تحلیل داده‌ها را شرح دهید.")),
        ("TitleNegar1", "یافته‌های پژوهش"),
        ("BodyNegar", hint("G_Ebtekar_Guide_Findings", "راهنمای یافته‌ها",
            "یافته‌ها را متناسب با اهداف و پرسش‌های پژوهش و با استفاده به‌جا از جدول و شکل ارائه کنید.")),
        ("TitleNegar1", "بحث و نتیجه‌گیری"),
        ("BodyNegar", hint("G_Ebtekar_Guide_Discussion", "راهنمای بحث و نتیجه‌گیری",
            "یافته‌ها را با پژوهش‌های پیشین مقایسه کنید، سپس نتیجه‌گیری و پیشنهادهای مبتنی بر یافته‌ها را بنویسید.")),
        ("TitleNegar1", "تقدیر و تشکر"),
        ("BodyNegar", hint("G_Ebtekar_Guide_Acknowledgment", "راهنمای تقدیر و تشکر",
            "در صورت لزوم از افراد یا نهادهای حامی تقدیر کنید؛ اگر موردی ندارید، این بخش را حذف کنید.")),
        ("TitleNegar1", "منابع"),
        ("RefNegar", hint("G_Ebtekar_Guide_References", "راهنمای منابع",
            "ابتدا منابع فارسی و سپس منابع لاتین را به ترتیب الفبا بنویسید (قالب APA). شماره‌گذاری نکنید.")),

        # 10_EnglishAbstract: new page, left-to-right
        ("TitleNegar", hint("TitleEn", "English title", "Article Title"),
         {"rtl": False, "page_break": True}),
        ("TitleNegarauthors", {"text": "authors Names", "bookmark": "authorsNamesEn"},
         {"rtl": False}),
        ("AbstractHeadNegar", "Abstract", {"rtl": False}),
        ("AbstractBodyNegar", hint("AbstractEn", "English abstract",
                                   "Type the abstract here.", block=True), {"rtl": False}),
        ("KeywordsNegar", [{"text": "Keywords: ", "bold": True},
                           hint("KeywordsEn", "English keywords",
                                "Separate keywords with commas.")],
         {"rtl": False, "align": "left"}),
    ],

    # ---- styles ----
    # based_on / next are style ids. Missing keys = inherit from based_on.
    "styles": {
        "BaseNegar": {"size": 12},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarauthors",
                       "font_cs": "B Nazanin", "size": 16, "bold": True,
                       "align": "center", "before": 12, "after": 12,
                       "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar",
                        "bold": True, "before": 12, "after": 6,
                        "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar",
                        "size": 12, "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar",
                        "size": 12, "outline": 2},
        "TitleNegarauthors": {"based_on": "BaseNegar", "size": 11,
                             "align": "center", "after": 12},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "size": 11, "bold": True, "before": 6, "after": 3,
                              "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "size": 11,
                              "align": "both", "after": 6},
        "KeywordsNegar": {"based_on": "BaseNegar", "size": 9,
                          "align": "both", "after": 12},
        "BodyNegar": {"based_on": "BaseNegar", "align": "both",
                      "after": 6, "first_line_cm": 0.5},
        "TableCaptionNegar": {"based_on": "BaseNegar", "size": 11,
                              "bold": True, "italic": True, "align": "center",
                              "before": 12, "after": 6, "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "size": 10,
                               "bold": True, "italic": True,
                               "align": "center", "after": 12},
        "TableTextNegar": {"based_on": "BaseNegar", "size": 9, "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "size": 11, "align": "both",
                     "after": 4, "left_cm": 0.5, "hanging_cm": 0.5},
    },
}
