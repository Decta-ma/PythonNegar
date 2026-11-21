
"""دریافت و بارگذاری قواعد جایگزینی از API و فایل‌های CSV سرور."""

import csv
import io
import json

from dataclasses import dataclass, field
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


# آدرس API اصلی
API_URL = "https://shivanegar.ir/api/getcsv"


# نام فایل‌های موردنیاز هر گروه
# ترتیب فایل‌ها مهم است؛ در تعارض، قاعده اولویت با فایل اول است.
RULE_GROUPS = {
    "half_space": [
        "HalfSpace1002.csv",
    ],
    "punctuation": [
        "Signs1000.csv",
        "Tashdid1000.csv",
        "Tanvin1000.csv",
    ],
    "spelling": [
        "SpellingCorrection1001.csv",
    ],
    "standard": [
        "Standard1004.csv",
    ],
}


# جانشین‌های داخل CSV که به نویسه واقعی تبدیل می‌شوند.
PLACEHOLDERS = {
    "^o": "\u200c",
}


REQUIRED_COLUMNS = (
    "Search",
    "Replace",
    "Wildcard",
    "MatchCase",
    "MatchWholeWord",
    "MatchKashida",
    "MatchDiacritics",
    "MatchAlefHamza",
    "CounterUp",
)


@dataclass(frozen=True)
class Rule:
    search: str
    replace: str
    wildcard: bool
    match_case: bool
    whole_word: bool
    kashida: bool
    diacritics: bool
    alef_hamza: bool
    count: bool
    source: str
    line: int


@dataclass
class RuleSet:
    rules: list = field(default_factory=list)
    skipped: list = field(default_factory=list)

    def summary(self):
        return f"{len(self.rules)} قاعده فعال، {len(self.skipped)} ردیف ردشده"


# کش آدرس‌های دریافتی از API
_csv_urls_cache = None

# کش قواعد پردازش‌شده هر گروه
_cache = {}


def _download(url):
    """دریافت محتوای یک آدرس از سرور."""

    request = Request(
        url,
        headers={
            "User-Agent": "PythonNegar/1.0",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            return response.read()

    except HTTPError as error:
        raise RuntimeError(
            f"سرور درخواست را نپذیرفت:\n"
            f"{url}\n"
            f"کد پاسخ: {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"ارتباط با سرور برقرار نشد:\n"
            f"{url}\n"
            f"جزئیات: {error.reason}"
        ) from error

    except (TimeoutError, OSError) as error:
        raise RuntimeError(
            f"دریافت اطلاعات از سرور با مشکل مواجه شد:\n"
            f"{url}\n"
            f"جزئیات: {error}"
        ) from error


def _get_csv_urls():
    """دریافت فهرست آدرس فایل‌های CSV از API."""

    global _csv_urls_cache

    if _csv_urls_cache is not None:
        return _csv_urls_cache

    content = _download(API_URL)

    try:
        data = json.loads(content.decode("utf-8-sig"))

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "پاسخ API معتبر نیست یا JSON قابل خواندن نیست."
        ) from error

    if str(data.get("status")) != "1":
        raise RuntimeError(
            f"دریافت فهرست فایل‌ها ناموفق بود.\n"
            f"وضعیت API: {data.get('status')}"
        )

    csv_urls = data.get("csv")

    if not isinstance(csv_urls, list):
        raise RuntimeError(
            "ساختار پاسخ API معتبر نیست؛ فهرست csv پیدا نشد."
        )

    # تبدیل فهرست آدرس‌ها به دیکشنری بر اساس نام فایل
    urls_by_name = {}

    for url in csv_urls:
        if not isinstance(url, str):
            continue

        filename = urlsplit(url).path.rsplit("/", 1)[-1]

        if filename:
            urls_by_name[filename.lower()] = url

    _csv_urls_cache = urls_by_name

    return _csv_urls_cache


def _flag(value):
    return (value or "").strip() == "1"


def _expand(text):
    for token, char in PLACEHOLDERS.items():
        text = text.replace(token, char)

    return text


def _read_url(url):
    """دریافت و خواندن ردیف‌های یک فایل CSV."""

    content = _download(url)

    try:
        text = content.decode("utf-8-sig")

    except UnicodeDecodeError as error:
        raise RuntimeError(
            f"کدگذاری فایل CSV معتبر نیست:\n{url}"
        ) from error

    reader = csv.DictReader(
        io.StringIO(text, newline="")
    )

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in (reader.fieldnames or [])
    ]

    if missing:
        filename = urlsplit(url).path.rsplit("/", 1)[-1]

        raise RuntimeError(
            f"ستون‌های لازم در فایل «{filename}» وجود ندارند:\n"
            f"{', '.join(missing)}"
        )

    for row in reader:
        yield reader.line_num, row


def load_group(group: str, data_dir=None) -> RuleSet:
    """قواعد یک گروه را از API دریافت و پردازش می‌کند."""

    if group not in RULE_GROUPS:
        raise RuntimeError(
            f"گروه قاعده ناشناخته: {group}"
        )

    # اگر قبلاً قواعد این گروه دریافت شده باشند، از کش استفاده می‌کنیم.
    if group in _cache:
        return _cache[group]

    # دریافت فهرست آدرس‌ها از API
    urls_by_name = _get_csv_urls()

    result = RuleSet()
    seen = {}

    for filename in RULE_GROUPS[group]:

        # پیدا کردن آدرس فایل موردنیاز در پاسخ API
        url = urls_by_name.get(filename.lower())

        if not url:
            raise RuntimeError(
                f"فایل «{filename}» در فهرست دریافتی از API پیدا نشد."
            )

        # خواندن قواعد فایل
        for line, row in _read_url(url):

            search = _expand(row["Search"] or "")
            replace = _expand(row["Replace"] or "")

            # ردیف خالی، جداکننده بصری است.
            if search == "":
                continue

            if search == replace:
                result.skipped.append(
                    (
                        filename,
                        line,
                        "بدون تغییر (Search = Replace)",
                        search,
                    )
                )
                continue

            # جلوگیری از قواعد تکراری یا متعارض
            if search in seen:

                reason = (
                    "تکراری"
                    if seen[search] == replace
                    else "تعارض با ردیف قبلی (نسخه اول استفاده می‌شود)"
                )

                result.skipped.append(
                    (filename, line, reason, search)
                )

                continue

            seen[search] = replace

            result.rules.append(
                Rule(
                    search=search,
                    replace=replace,
                    wildcard=_flag(row["Wildcard"]),
                    match_case=_flag(row["MatchCase"]),
                    whole_word=_flag(row["MatchWholeWord"]),
                    kashida=_flag(row["MatchKashida"]),
                    diacritics=_flag(row["MatchDiacritics"]),
                    alef_hamza=_flag(row["MatchAlefHamza"]),
                    count=_flag(row["CounterUp"]),
                    source=filename,
                    line=line,
                )
            )

    # ذخیره نتیجه برای استفاده‌های بعدی
    _cache[group] = result

    return result


def clear_cache():
    """پاک کردن کش برای دریافت مجدد فهرست و قواعد از سرور."""

    global _csv_urls_cache

    _csv_urls_cache = None
    _cache.clear()
