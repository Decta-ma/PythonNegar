import re 
MIN_LENGTH = 3
EMAIL_RE = re.compile(
        r"[A-Za-z0-9_%+-]+(\.[A-Za-z0-9_%+-]+)*"
        r"@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
)

def validate_required_text(text):
    text = (text or "").strip()
    if not text:
        return "فیلد نباید خالی باشد"
    if len(text) < MIN_LENGTH:
        return "حداقل 3 حرف وارد کنید"
    return None 

def validate_email(email, required=False):
    email = (email or "").strip()
    if not email :
        return "ایمیل الزامی است" if required else None
    if not EMAIL_RE.fullmatch(email):
        return "ساختار ایمیل معتبر نیست"
    return None

def normalize_orcid(text):
    value = (text or "").strip()
    value = re.sub(r"^(https?://)?(www\.)?orcid\.org/", "", value, flags=re.IGNORECASE)
    value = value.replace("-", "").replace(" ", "").upper()
    if not re.fullmatch(r"\d{15}[\dX]", value):
        return None
    return f"{value[0:4]}-{value[4:8]}-{value[8:12]}-{value[12:16]}"


def validate_authors(author, others=()):
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
