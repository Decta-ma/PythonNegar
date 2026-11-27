"""Config (data only) for JRORS - The Journal of Radar and Optical Remote Sensing and GIS.

Values read from JRORS.dotm: US Letter, margins top 3.0 cm, sides and bottom 2.5 cm,
Times New Roman 12 pt, LTR, different first page, even/odd headers.
Colours (green headings 538135, orange abstract heading C45911) are read from styles.xml.
Header text is taken from header1.xml (first page) and header2.xml (running title).
"""

from ._parts import field, hint

JRORS = {
    "id": "JRORS",
    "name": "The Journal of Radar and Optical Remote Sensing and GIS",
    "short_name": "JRORS",

    "page": {
        "width_cm": 21.59, "height_cm": 27.94,          # US Letter
        "margin_top": 3.0, "margin_right": 2.5,
        "margin_bottom": 2.5, "margin_left": 2.5,
        "header_distance": 1.27, "footer_distance": 1.27,
        "rtl": False,
        "different_first_page": True,
        "even_odd_headers": True,
    },

    "fonts": {"latin": "Times New Roman", "complex": "Times New Roman", "base_size": 12},

    "header": {
        "line1": "The Journal of Radar and Optical Remote Sensing and GIS, Volume …, Issue …",
        "line2": "Running title of paper | Author name, et al.",
        "size": 9, "border": True, "per_kind": True,
    },

    "skeleton": [
        ("TitleNegar", hint("TitleEn", "Article title", "Article Title")),
        ("TitleNegarAuthor", {"text": "Author Names", "bookmark": "AuthorNamesEn"}),

        ("AbstractHeadNegar", "Article Info"),
        ("AbstractBodyNegar", [{"text": "Article type: ", "bold": True},
                               hint("ArticleType", "Article type", "Research article")]),
        ("AbstractBodyNegar", [{"text": "Article history:", "bold": True}]),
        ("AbstractBodyNegar", [{"text": "Received: ", "bold": True},
                               field("JournalReceivedDate", "Received date", "//")]),
        ("AbstractBodyNegar", [{"text": "Received in revised form: ", "bold": True},
                               field("JournalRevisedDate", "Revised date", "//")]),
        ("AbstractBodyNegar", [{"text": "Accepted: ", "bold": True},
                               field("JournalAcceptedDate", "Accepted date", "//")]),
        ("AbstractBodyNegar", [{"text": "Published online: ", "bold": True},
                               field("JournalPublishedDate", "Published date", "//")]),

        ("AbstractHeadNegar", "ABSTRACT"),
        ("AbstractBodyNegar", hint("AbstractEn", "Abstract",
                                   "Objective, methods, results and conclusion.", block=True)),
        ("KeywordsNegar", [{"text": "Keywords: ", "bold": True},
                           hint("KeywordsEn", "Keywords", "Separate keywords with commas.")]),

        ("TitleNegar1", "Introduction"),
        ("BodyNegar", hint("G_JRORS_Guide_Introduction", "Introduction guide",
                           "Introduce the topic, state the problem and its significance, review relevant work briefly, and state the aim of the study.")),
        ("TitleNegar1", "Materials and Methods"),
        ("BodyNegar", hint("G_JRORS_Guide_MaterialsAndMethods", "Methods guide",
                           "Describe materials, data, procedures and analysis in enough detail for the study to be reproduced.")),
        ("TitleNegar1", "Results"),
        ("BodyNegar", hint("G_JRORS_Guide_Results", "Results guide",
                           "Present the results in a logical order, using tables and figures where helpful. Avoid interpretation here.")),
        ("TitleNegar1", "Discussion"),
        ("BodyNegar", hint("G_JRORS_Guide_Discussion", "Discussion guide",
                           "Interpret the results, compare them with previous studies, and discuss limitations.")),
        ("TitleNegar1", "Conclusion"),
        ("BodyNegar", hint("G_JRORS_Guide_Conclusion", "Conclusion guide",
                           "State the main conclusions that follow from the results and their implications.")),
        ("TitleNegar1", "Author Contributions"),
        ("BodyNegar", hint("G_JRORS_Guide_AuthorContributions", "Contributions guide",
                           "Describe each author’s contribution (e.g. conceptualization, methodology, analysis, writing).")),
        ("TitleNegar1", "Data Availability Statement"),
        ("BodyNegar", hint("G_JRORS_Guide_DataAvailability", "Data availability guide",
                           "State where the data supporting the findings can be accessed, or why they are not available.")),
        ("TitleNegar1", "Acknowledgements"),
        ("BodyNegar", hint("G_JRORS_Guide_Acknowledgements", "Acknowledgements guide",
                           "Thank people or institutions that supported the work. Delete this section if not needed.")),
        ("TitleNegar1", "Ethical considerations"),
        ("BodyNegar", hint("G_JRORS_Guide_EthicalConsiderations", "Ethics guide",
                           "Describe ethical approvals and consent procedures, or state that none were required.")),
        ("TitleNegar1", "Funding"),
        ("BodyNegar", hint("G_JRORS_Guide_Funding", "Funding guide",
                           "State the funding sources and grant numbers, or declare that there was no funding.")),
        ("TitleNegar1", "Conflict of interest"),
        ("BodyNegar", hint("G_JRORS_Guide_ConflictOfInterest", "Conflict of interest guide",
                           "Declare any competing interests, or state that the authors have none.")),
        ("TitleNegar1", "References"),
        ("RefNegar", hint("G_JRORS_Guide_References", "References guide",
                          "List references in the journal style; every in-text citation must appear here and vice versa.")),
    ],

    "styles": {
        "BaseNegar": {"font": "Times New Roman", "size": 12},
        "TitleNegar": {"based_on": "BaseNegar", "next": "TitleNegarAuthor", "size": 16,
                       "bold": True, "align": "center", "before": 6, "after": 6, "keep_next": True},
        "TitleNegar1": {"based_on": "BaseNegar", "next": "BodyNegar", "bold": True,
                        "color": "538135", "size": 14, "before": 12, "after": 4, "line": 1.2,
                        "keep_next": True, "outline": 0},
        "TitleNegar2": {"based_on": "TitleNegar1", "next": "BodyNegar", "size": 13,
                        "keep_next": True, "outline": 1},
        "TitleNegar3": {"based_on": "TitleNegar2", "next": "BodyNegar", "size": 12,
                        "bold": False, "italic": True, "outline": 2},
        "TitleNegarAuthor": {"based_on": "BaseNegar", "size": 11, "bold": True, "align": "center"},
        "AbstractHeadNegar": {"based_on": "BaseNegar", "next": "AbstractBodyNegar",
                              "bold": True, "color": "C45911", "keep_next": True},
        "AbstractBodyNegar": {"based_on": "BaseNegar", "size": 10, "after": 4,
                              "line": 1.2, "align": "both"},
        "KeywordsNegar": {"based_on": "BaseNegar", "size": 10, "align": "both",
                          "left_cm": 0.5, "hanging_cm": 0.5},
        "BodyNegar": {"based_on": "BaseNegar", "after": 6, "line": 1.2,
                      "first_line_cm": 0.5, "align": "both"},
        "TableCaptionNegar": {"based_on": "BaseNegar", "size": 10, "bold": True,
                              "align": "center", "before": 6, "after": 3, "keep_next": True},
        "FigureCaptionNegar": {"based_on": "BaseNegar", "size": 10, "bold": True,
                               "align": "center", "before": 3, "after": 6},
        "TableTextNegar": {"based_on": "BaseNegar", "size": 10, "align": "center"},
        "RefNegar": {"based_on": "BaseNegar", "next": "RefNegar", "size": 11,
                     "align": "both", "before": 4, "after": 4, "line": 1.2,
                     "left_cm": 1.0, "hanging_cm": 1.0},
        "FootnoteText": {"based_on": "BaseNegar", "size": 9, "align": "left"},
    },
}

JOURNAL = JRORS