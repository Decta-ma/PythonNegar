import pytest

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



def validate_author(author, others=()):
    """نویسنده را بررسی می‌کند. خروجی: لیست پیام‌های خطا (خالی یعنی سالم)."""
    errors = []

    for label, value in (("نام نویسنده", author.name_fa),
                         ("نام انگلیسی نویسنده", author.name_en)):
        msg = validate_required_text(value)
        if msg:
            errors.append(f"{label}: {msg}")

    msg = validate_email(author.email, required=author.is_responsible)
    if msg:
        errors.append(msg)

    if author.orcid and normalize_orcid(author.orcid) is None:
        errors.append("شناسه ارکید معتبر نیست. قالب صحیح: 0000-0000-0000-0000")

    others = [o for o in others if o is not author]

    email = author.email.strip().lower()
    if email and any(o.email.strip().lower() == email for o in others):
        errors.append("این ایمیل قبلاً برای نویسنده دیگری ثبت شده است.")

    if author.is_responsible and any(o.is_responsible for o in others):
        errors.append("قبلاً یک نویسنده مسئول ثبت شده است.")

    return errors
