from app.article.models import Author, Affiliation, ArticleInfo, UniversityType
from app.article.validators import normalize_orcid
from app.article.word_fill import fill_document

def build_university_type(value):
    value = (value or "").strip()
    if not value:
        return None
    return UniversityType(value)


def build_author(form):
    return Author(
        name_fa=form.get("name_fa", "").strip(),
        name_en=form.get("name_en", "").strip(),
        email=form.get("email", "").strip(),
        orcid=build_orcid(form.get("orcid", "")),
        is_responsible=bool(form.get("is_responsible", False)),
        affiliation=build_affiliation(form)
    )


def build_affiliation(form):
    return Affiliation(
        university_type=build_university_type(form.get("university_type", "")),
        degree_fa=form.get("degree_fa", "").strip(),
        degree_en=form.get("degree_en", "").strip(),
        group_fa=form.get("group_fa", "").strip(),
        group_en=form.get("group_en", "").strip(),
        faculty_fa=form.get("faculty_fa", "").strip(),
        faculty_en=form.get("faculty_en", "").strip(),
        university_fa=form.get("university_fa", "").strip(),
        university_en=form.get("university_en", "").strip(),
        city_fa=form.get("city_fa", "").strip(),
        city_en=form.get("city_en", "").strip()
    )


def build_article_info(form):
    return ArticleInfo(
        journal_id=form.get("journal_id", "").strip(),
        title_fa=form.get("title_fa", "").strip(),
        title_en=form.get("title_en", "").strip(),
        authors=[build_author(m) for m in form.get("authors", [])]
    )


def create_article(engine, form, out_path, template_path):
    """از دیکشنری فرم، سند Word می‌سازد و پر می‌کند. نام سند را برمی‌گرداند."""
    info = build_article_info(form)
    doc_name = engine.create_new_signed_doc(out_path, template_path=str(template_path))
    fill_document(engine.doc, info)
    return doc_name

def build_orcid(value):
    value = (value or "").strip()
    return normalize_orcid(value) or value
