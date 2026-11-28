from app.article.models import UniversityType
from app.article.wizard import build_author


def test_build_author_new_fields():
    form = {
        "name_fa": "علی رضایی",
        "name_en": "Ali Rezaei",
        "orcid": "https://orcid.org/0000000218250097",
        "is_responsible": True,
        "university_type": "azad",
    }
    author = build_author(form)
    assert author.orcid == "0000-0002-1825-0097"
    assert author.is_responsible is True
    assert author.affiliation.university_type is UniversityType.AZAD


def test_build_author_defaults():
    author = build_author({"name_fa": "الف", "name_en": "A"})
    assert author.orcid == ""
    assert author.is_responsible is False
    assert author.affiliation.university_type is None