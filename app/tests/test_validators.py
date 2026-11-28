import pytest
from app.article.models import Author
from app.article.validators import validate_authors

from app.article.validators import (
        validate_required_text, 
        validate_email,
        normalize_orcid
)

def test_required_text_empty():
    assert validate_required_text("") == "فیلد نباید خالی باشد"

def test_required_text_too_short():
    assert validate_required_text("    ab    ") == "حداقل 3 حرف وارد کنید"

def test_required_text_ok():
    assert validate_required_text("ali") is None 

@pytest.mark.parametrize("email, expected", [
    ("", None),
    ("ali@mail.com", None),
    ("ali@mail", "ساختار ایمیل معتبر نیست"),
    ])
def test_validate_email(email, expected):
    assert validate_email(email) == expected


def make_author(**kwargs):
    base = {"name_fa": "علی رضایی", "name_en": "Ali Rezaei"}
    base.update(kwargs)
    return Author(**base)


def test_validate_author_ok():
    assert validate_authors(make_author()) == []


def test_responsible_needs_email():
    assert validate_authors(make_author(is_responsible=True)) == ["ایمیل الزامی است"]


def test_invalid_orcid():
    errors = validate_authors(make_author(orcid="123"))
    assert len(errors) == 1 and "ارکید" in errors[0]


def test_duplicate_email():
    a = make_author(email="ali@mail.com")
    b = make_author(name_fa="رضا احمدی", name_en="Reza Ahmadi", email="ALI@mail.com")
    assert validate_authors(b, others=[a]) == [
        "این ایمیل قبلاً برای نویسنده دیگری ثبت شده است."
    ]


def test_two_responsible():
    a = make_author(email="a@mail.com", is_responsible=True)
    b = make_author(name_fa="رضا احمدی", name_en="Reza Ahmadi",
                    email="b@mail.com", is_responsible=True)
    assert validate_authors(b, others=[a]) == ["قبلاً یک نویسنده مسئول ثبت شده است."]
    

@pytest.mark.parametrize("text, expected", [
    ("0000-0002-1825-0097", "0000-0002-1825-0097"),
    ("https://orcid.org/0000000218250097", "0000-0002-1825-0097"),
    ("0000 0002 1825 009x", "0000-0002-1825-009X"),
    ("123", None),
    ("", None),
])
def test_normalize_orcid(text, expected):
    assert normalize_orcid(text) == expected