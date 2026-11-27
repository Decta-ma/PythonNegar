"""Config (data only) for AIT - Journal of Artificial Intelligence Tools in Software and Data Engineering (AITSDE).

English, LTR, A4. Values read from AIT.dotm: page 21.0 x 29.7 cm; top/right/bottom 2.0 cm,
left 2.5 cm; header/footer distance 0.76 cm; different first page. Fonts TNR, sizes from styles.xml
(estimates for base sizes). Header line 1 on first page, running title on other pages.
"""

from ._parts import field, hint

AIT = {
    "id": "AIT",
    "name": "Journal of Artificial Intelligence Tools in Software and Data Engineering",
    "short_name": "AITSDE",

    "page": {
        "width_cm": 21.0, "height_cm": 29.7,
        "margin_top": 2.0, "margin_right": 2.0,
        "margin_bottom": 2.0, "margin_left": 2.5,
        "header_distance": 0.76, "footer_distance": 0.76,
        "rtl": False,
        "different_first_page": True,
        "even_odd_headers": False,
    },

    "fonts": {"latin": "Times New Roman", "complex": "Times New Roman", "base_size": 11},

    "header": {
        "line1": "Journal of Artificial Intelligence Tools in Software and Data Engineering (AITSDE), Volume … , Issue … ",
        "line2": "Running title of paper | Author name, et al.",
        "size": 9, "border": False, "per_kind": True,
    },

    "skeleton": [
        ("TitleNegar", hint("TitleEn", "Article title", "Article Title")),
        ("TitleNegarAuthor", {"text": "Author Names", "bookmark": "AuthorNamesEn"}),

        ("AbstractHeadNegar", "Abstract"),
        ("AbstractBodyNegar", hint("AbstractEn", "Abstract", "Abstract text goes here.", block=True)),
        ("KeywordsNegar", [{"text": "Keywords: ", "bold": True},
                           hint("KeywordsEn", "Keywords", "keyword one; keyword two")]),

        ("TitleNegar1", "1. Introduction"),
        ("BodyNegar", hint("G_AIT_Guide_Introduction", "Introduction guide",
                           "Describe the problem, its significance, background and the aims of the study.")),
        ("TitleNegar1", "2. Conclusion"),
        ("BodyNegar", hint("G_AIT_Guide_Conclusion", "Conclusion guide",
                           "Summarize the main findings, limitations and suggestions for future work.")),
        ("TitleNegar1", "Acknowledgment"),
        ("RefNegar", hint("G_AIT_Guide_Acknowledgment", "Acknowledgment guide",
                          "Acknowledge funders or supporters if any; otherwise delete this section.")),
        ("TitleNegar1", "References"),
        ("RefNegar", hint("G_AIT_Guide_References", "References guide",
                          "List references in the journal's citation style.")),
    ],

    "styles": {
        "BaseNegar": {"font": "Times New Roman", "size": 11},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor", "size": 24,
                       "bold": True, "align": "center", "before": 6, "after": 6, "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar", "size": 12, "bold": True,
                        "align": "left", "before": 8, "after": 3, "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar", "size": 11,
                        "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar", "size": 11,
                        "italic": True, "outline": 2},
        "TitleNegarAuthor": {"based_on": "BaseNegar", "size": 11, "align": "center",
                             "before": 6, "after": 6},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "size": 11, "bold": True, "align": "left", "before": 8,
                              "after": 3, "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "size": 10, "align": "both"},
        "KeywordsNegar": {"based_on": "BaseNegar", "size": 10, "align": "left",
                          "before": 4, "after": 6},
        "BodyNegar": {"based_on": "BaseNegar", "next": "BodyNegar", "size": 11,
                      "align": "both", "before": 0, "after": 6, "first_line_cm": 0.5},
        "TableCaptionNegar": {"based_on": "BaseNegar", "size": 10, "bold": True,
                              "align": "center", "before": 6, "after": 2, "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "size": 10, "align": "center",
                               "before": 2, "after": 6},
        "TableTextNegar": {"based_on": "BaseNegar", "size": 9, "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "next": "RefNegar", "size": 10,
                     "align": "both", "before": 0, "after": 3,
                     "left_cm": 0.75, "hanging_cm": 0.75},
        "FootnoteText": {"based_on": "BaseNegar", "size": 9, "align": "left"},
    },
}

JOURNAL = AIT
