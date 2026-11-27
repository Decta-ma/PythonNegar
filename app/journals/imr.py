"""Config (data only) for the IMR journal template (پژوهش های بازاریابی اسلامی).

Units: margins in cm, font sizes in pt, spacing in pt, indents in cm.
IMR has no header text and no different first page (same as the original .dotm).
"""

from ._parts import field, hint

_BLUE = "3333FF"

IMR = {
    "id": "IMR",
    "name": "پژوهش های بازاریابی اسلامی",
    "short_name": "پژوهش های بازاریابی اسلامی",

    "page": {
        "width_cm": 21.0, "height_cm": 29.7,
        "margin_top": 2.54, "margin_right": 2.54,
        "margin_bottom": 2.54, "margin_left": 2.54,
        "header_distance": 1.25, "footer_distance": 1.25,
        "rtl": True,
        "different_first_page": False,
        "even_odd_headers": False,
    },

    "fonts": {"latin": "IRLotus", "complex": "IRLotus", "base_size": 12},

    # empty header text, as in the original
    "header": {"line1": "", "line2": "", "size": 10, "border": False},

    "skeleton": [
        ("TitleNegar", hint("TitleFa", "عنوان فارسی مقاله", "عنوان مقاله")),
        ("TitleNegarAuthor", {"text": "نام نویسندگان", "bookmark": "AuthorNamesFa"}),
        ("BodyNegar", [{"text": "تاریخ دریافت: ", "bold": True},
                       field("JournalReceivedDate", "Received date", "//"),
                       {"text": "     تاریخ پذیرش: ", "bold": True},
                       field("JournalAcceptedDate", "Accepted date", "//"),
                       {"text": "     تاریخ انتشار آنلاین: 01/01/1401", "bold": True}],
         {"align": "left"}),

        ("AbstractHeadNegar", "چکیده"),
        ("AbstractBodyNegar", "چکیده باید مختصر، روان و گویا باشد (حداقل ۱۵۰ و حداکثر ۲۵۰ کلمه) و در چهار بخش زیر بیان شود."),
        ("AbstractBodyNegar", hint("G_IMR_Abs_Purpose", "هدف", "هدف/ سئوال اصلی: هدف یا سؤال اصلی پژوهش را در یک یا دو جمله بنویسید.")),
        ("AbstractBodyNegar", hint("G_IMR_Abs_Method", "روش پژوهش", "روش پژوهش: نوع پژوهش و روش گردآوری و تحلیل داده‌ها را به‌طور خلاصه بنویسید.")),
        ("AbstractBodyNegar", hint("G_IMR_Abs_Findings", "یافته‌ها", "یافته‌ها: مهم‌ترین یافته‌ها و نتایج پژوهش را خلاصه کنید.")),
        ("AbstractBodyNegar", hint("G_IMR_Abs_Conclusion", "بحث و نتیجه‌گیری", "بحث و نتیجه‌گیری: نتیجهٔ اصلی و پیام کلیدی مقاله را بنویسید.")),
        ("KeywordsNegar", [{"text": "واژه‌های کلیدی: ", "bold": True},
                           hint("KeywordsFa", "واژه‌های کلیدی",
                                "کلیدواژه‌ها را با ویرگول از هم جدا کنید.")]),

        ("TitleNegar1", "مقدمه"),
        ("BodyNegar", hint("G_IMR_Intro_Preface", "دیباچه موضوع", "دیباچه موضوع: شروع بحث و بیان موضوع را با توجه به حوزه و رشتهٔ کلی مورد بحث و مباحث روز بنویسید.")),
        ("BodyNegar", hint("G_IMR_Intro_Necessity", "ضرورت موضوع", "ضرورت موضوع: نیازها و ضرورت موضوع مقاله را با توجه به مطالعات پیشین و شواهد موجود بیان کنید.")),
        ("BodyNegar", hint("G_IMR_Intro_Importance", "اهمیت موضوع", "اهمیت موضوع: اهمیت، فواید و کارکردهای نظری و عملی بررسی موضوع مقاله را بنویسید.")),
        ("BodyNegar", hint("G_IMR_Intro_Problem", "مساله اصلی", "مساله اصلی (بیان مسأله): مسئله و پرسش یا پرسش‌های اصلی مقاله و هدف یا اهداف آن را روشن و کامل بیان کنید.")),

        ("TitleNegar1", "ادبیات موضوع و پیشینه"),
        ("BodyNegar", hint("G_IMR_Bg_Theory", "ادبیات نظری", "ادبیات نظری: چارچوب نظری، مبانی نظری و نظریه‌ها را ارائه کنید؛ مطالب باید جامع، کاربردی و مرتبط با پرسش‌ها و اهداف مقاله باشند.")),
        ("BodyNegar", hint("G_IMR_Bg_Review", "پیشینه پژوهش", "پیشینه پژوهش: مطالعات و مقالات پیشین مرتبط را دسته‌بندی کنید و با ارتباط منطقی مرور کنید.")),
        ("BodyNegar", hint("G_IMR_Bg_Novelty", "وجه نوآوری", "وجه نوآوری مقاله حاضر نسبت به مطالعات پیشین: نوآوری و وجه تمایز پژوهش را با مطالعات پیشین روشن بنویسید.")),

        ("TitleNegar1", "روش تحقیق"),
        ("BodyNegar", hint("G_IMR_Me_Type", "نوع تحقیق", "نوع تحقیق: تحقیق بنیادی، توسعه‌ای یا کاربردی بودن را با ذکر دلیل بنویسید.")),
        ("BodyNegar", hint("G_IMR_Me_Strategy", "استراتژی کلی تحقیق", "استراتژی کلی تحقیق: کمی یا کیفی بودن تحقیق و شیوهٔ آن و دلیل انتخاب این شیوه را بیان کنید.")),
        ("BodyNegar", hint("G_IMR_Me_Collection", "روش‌های گردآوری داده‌ها", "روش‌های گردآوری داده‌ها: روش‌های گردآوری داده‌ها (پیمایشی، کتابخانه‌ای و...) را هر کدام با ذکر دلیل بنویسید.")),
        ("BodyNegar", hint("G_IMR_Me_Analysis", "روش‌های تحلیل داده‌ها", "روش‌های تحلیل داده‌ها: روش‌های تحلیل و دلیل برتری آن‌ها را بنویسید؛ توضیح آموزشی روش لازم نیست و فقط فرمول‌های ضروری ذکر شود.")),
        ("BodyNegar", hint("G_IMR_Me_Sample", "جامعه و نمونه آماری", "جامعه و نمونه آماری: جامعهٔ آماری و دلیل انتخاب آن، روش نمونه‌گیری و حجم نمونه را معرفی کنید.")),
        ("BodyNegar", hint("G_IMR_Me_Tool", "ابزار جمع آوری داده", "ابزار جمع آوری داده و روایی و پایایی آن: ابزار و منبع آن و چگونگی سنجش روایی و پایایی را شرح دهید.")),
        ("BodyNegar", hint("G_IMR_Me_Steps", "مراحل انجام", "مراحل انجام و بکارگیری روش: فرایند انجام تحقیق را مختصر و مفید شرح دهید.")),

        ("TitleNegar1", "یافته‌های تحقیق"),
        ("BodyNegar", hint("G_IMR_Findings", "راهنمای یافته‌ها", "یافته‌های حاصل از روش‌شناسی را دسته‌بندی و منطقی و متناسب با اهداف و پرسش‌های مقاله ارائه دهید؛ ترتیب بیان مطالب مطابق «مراحل انجام و بکارگیری روش» باشد.")),

        ("TitleNegar1", "بحث و نتیجه‌گیری"),
        ("BodyNegar", hint("G_IMR_Di_Discussion", "بحث", "بحث: یافته‌های مقاله را با نتایج مطالعات پیشین مقایسه کنید و دلایل شباهت و تفاوت آن‌ها را بیان کنید.")),
        ("BodyNegar", hint("G_IMR_Di_Conclusion", "نتیجه‌گیری", "نتیجه‌گیری: نتیجه‌ای مشخص، مختصر و قابل استفاده ارائه دهید که با یافته‌ها و اهداف مقاله ارتباط منطقی داشته باشد.")),
        ("BodyNegar", hint("G_IMR_Di_Suggestions", "پیشنهادها", "پیشنهادها: پیشنهادها باید مبتنی بر یافته‌های مقاله و در راستای توسعهٔ نظری یا کاربردی آن‌ها باشند؛ از پیشنهادهای بدیهی خودداری کنید.")),

        ("TitleNegar1", "منابع"),
        ("BodyNegar", "منابع فارسی"),
        ("RefNegar", hint("G_IMR_Ref_Fa", "منابع فارسی", "منابع فارسی را به ترتیب حروف الفبا بنویسید. الگو: نام‌خانوادگی، نام (سال انتشار). عنوان مقاله. نام نشریه، دوره (شماره)، صفحه.")),
        ("BodyNegar", "منابع لاتین"),
        ("RefNegar", hint("G_IMR_Ref_En", "منابع لاتین", "List in alphabetical order, APA format: Author, A. A. (Year). Title of article. Journal Name, volume(issue), pages."),
         {"rtl": False, "align": "left"}),

        # English abstract: new page, left-to-right
        ("TitleNegar", hint("TitleEn", "English title", "Article Title"),
         {"rtl": False, "page_break": True, "before": 0}),
        ("TitleNegarAuthor", {"text": "Author Names", "bookmark": "AuthorNamesEn"}, {"rtl": False}),
        ("BodyNegar", [{"text": "Received: 09/06/2021     Accept: 03/10/2021     Online Publish: 01/12/2021", "bold": True}],
         {"rtl": False, "align": "left"}),
        ("AbstractHeadNegar", "Abstract", {"rtl": False, "align": "left"}),
        ("AbstractBodyNegar", "150 to 250 words, in the four sections below; an exact translation of the Persian abstract.", {"rtl": False, "align": "both"}),
        ("AbstractBodyNegar", hint("G_IMR_AbsEn_Purpose", "Purpose", "Purpose: State the main aim or research question of the study."), {"rtl": False, "align": "both"}),
        ("AbstractBodyNegar", hint("G_IMR_AbsEn_Method", "Methodology", "Methodology: Briefly describe the research design, data collection and data analysis."), {"rtl": False, "align": "both"}),
        ("AbstractBodyNegar", hint("G_IMR_AbsEn_Findings", "Findings", "Findings: Summarize the most important findings of the study."), {"rtl": False, "align": "both"}),
        ("AbstractBodyNegar", hint("G_IMR_AbsEn_Conclusion", "Conclusion", "Conclusion: State the main conclusion and its implications."), {"rtl": False, "align": "both"}),
        ("KeywordsNegar", [{"text": "Keywords: ", "bold": True},
                           hint("KeywordsEn", "English keywords", "3 to 5 keywords, separated by commas.")],
         {"rtl": False, "align": "left"}),
    ],

    "styles": {
        "BaseNegar": {"font": "IRLotus", "size": 12, "after": 0},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor",
                       "font": "IRMitra", "size": 16, "bold": True, "color": _BLUE,
                       "align": "center", "before": 114, "after": 6, "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar",
                        "font": "IRLotus", "size": 13, "bold": True, "color": _BLUE,
                        "before": 14, "after": 0, "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar",
                        "size": 12, "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar",
                        "size": 12, "outline": 2},
        "TitleNegarAuthor": {"based_on": "BaseNegar", "font": "IRMitra",
                             "size": 12, "align": "center", "after": 0},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "font": "IRMitra", "size": 13, "bold": True,
                              "color": _BLUE, "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "font": "IRMitra",
                              "size": 12, "align": "both"},
        "KeywordsNegar": {"based_on": "BaseNegar", "font": "IRMitra",
                          "size": 12, "align": "both"},
        "BodyNegar": {"based_on": "BaseNegar", "next": "BodyNegar",
                      "font": "IRLotus", "size": 12, "align": "both"},
        "TableCaptionNegar": {"based_on": "BaseNegar", "font": "IRLotus", "size": 10,
                              "bold": True, "align": "center", "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "font": "IRLotus", "size": 10,
                               "bold": True, "align": "center"},
        "TableTextNegar": {"based_on": "BaseNegar", "font": "IRLotus", "size": 10,
                           "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "next": "RefNegar", "font": "IRLotus",
                     "size": 12, "align": "both"},
        "FootnoteTextFa": {"based_on": "BaseNegar", "font": "IRMitra", "size": 10, "align": "right"},
        "FootnoteTextEn": {"based_on": "BaseNegar", "font": "IRMitra", "size": 10, "align": "left"},
    },
}

JOURNAL = IMR