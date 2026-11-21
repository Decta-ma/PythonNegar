"""Config (data only) for the Ebtekar journal template.

Change a number here, build again, and the .dotm changes.
Units: margins in cm, font sizes in pt, spacing in pt, indents in cm.
"""

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

    # ---- styles ----
    # based_on / next are style ids. Missing keys = inherit from based_on.
    "styles": {
        "BaseNegar": {"size": 12},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor",
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
        "TitleNegarAuthor": {"based_on": "BaseNegar", "size": 11,
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
