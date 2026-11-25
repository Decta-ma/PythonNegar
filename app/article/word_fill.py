"""جایگذاری اطلاعات ویزارد در سند ساخته‌شده (معادل FillDocumentContent در C#)."""

# ثابت‌های Word
WD_RESTART_PAGE = 2        # WdNumberingRule.wdRestartPage
WD_RTL = 0                 # WdReadingOrder.wdReadingOrderRtl
WD_LTR = 1                 # WdReadingOrder.wdReadingOrderLtr
WD_ALIGN_LEFT = 0          # WdParagraphAlignment.wdAlignParagraphLeft
WD_LANG_ENGLISH_US = 1033  # WdLanguageID.wdEnglishUS


def set_content_control_text(doc, tag, text):
    """متن Content Control با تگ مشخص را عوض می‌کند. اگر پیدا نشد False."""
    for cc in doc.ContentControls:
        if cc.Tag == tag:
            cc.Range.Text = text
            return True
    return False


def affiliation_text(affiliation, english):
    """متن پاورقی وابستگی علمی (موقتی: ترتیب نهایی را از C# اسلاید ۵ می‌گیریم)."""
    a = affiliation
    if english:
        parts = [a.degree_en, a.group_en, a.faculty_en, a.university_en, a.city_en]
        sep = ", "
    else:
        parts = [a.degree_fa, a.group_fa, a.faculty_fa, a.university_fa, a.city_fa]
        sep = "، "
    text = sep.join(p.strip() for p in parts if p and p.strip())
    if text:
        return text
    return "Affiliation not specified" if english else "وابستگی علمی مشخص نیست"


def apply_footnote_direction(footnote, english):
    """جهت و استایل پاورقی: انگلیسی LTR و چپ‌چین، فارسی RTL."""
    style = "FootnoteTextEn" if english else "FootnoteTextFa"
    wanted = WD_LTR if english else WD_RTL
    try:
        rng = footnote.Range
        try:
            rng.Style = style
        except Exception:
            print(f"[FN] استایل {style} اعمال نشد")
        if english:
            rng.LanguageID = WD_LANG_ENGLISH_US
        for p in rng.Paragraphs:
            if p.Style.NameLocal != style or p.ReadingOrder != wanted:
                p.Reset()
                p.ReadingOrder = wanted
                if english:
                    p.Alignment = WD_ALIGN_LEFT
    except Exception as exc:
        print(f"[FN] خطا در جهت پاورقی: {exc}")


def insert_authors(doc, bookmark_name, authors, english):
    """نام نویسندگان را در بوکمارک می‌نویسد و برای هرکدام پاورقی می‌سازد."""
    if not authors or not doc.Bookmarks.Exists(bookmark_name):
        return

    rng = doc.Bookmarks(bookmark_name).Range
    pos = rng.Start
    rng.Text = ""  # متن قبلی (placeholder) پاک شود
    doc.Footnotes.NumberingRule = WD_RESTART_PAGE

    created = []
    for i, author in enumerate(authors):
        if i > 0:
            r = doc.Range(pos, pos)
            r.InsertAfter(", " if english else "، ")
            pos = r.End

        name = (author.name_en if english else author.name_fa) or ""
        r = doc.Range(pos, pos)
        r.InsertAfter(name.strip() or "-")
        pos = r.End

        note = affiliation_text(author.affiliation, english)
        footnote = doc.Footnotes.Add(Range=doc.Range(pos, pos), Text=note)
        created.append(footnote)
        pos = footnote.Reference.End

    for footnote in created:
        apply_footnote_direction(footnote, english)


def fill_document(doc, info):
    """info: ArticleInfo. بعد از جایگذاری سند ذخیره می‌شود."""
    set_content_control_text(doc, "TitleFa", info.title_fa)
    set_content_control_text(doc, "TitleEn", info.title_en)
    insert_authors(doc, "AuthorNamesFa", info.authors, english=False)
    insert_authors(doc, "AuthorNamesEn", info.authors, english=True)
    doc.Save()