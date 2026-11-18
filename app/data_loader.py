"""بارگذاری قواعد جایگزینی (Find & Replace) از فایل‌های CSV پوشهٔ app/data.

هر ردیف CSV یک قاعده است با ستون‌های:
Search, Replace, Wildcard, MatchCase, MatchWholeWord,
MatchKashida, MatchDiacritics, MatchAlefHamza, CounterUp

نکته‌های مهم:
  * فاصله‌های ابتدا و انتهای Search/Replace معنی دارند (مثلاً " می ")؛ هرگز strip نمی‌شوند.
  * ردیف‌های با Search خالی جداکنندهٔ بصری‌اند و نادیده گرفته می‌شوند.
  * ستون‌های پرچم اگر خالی باشند، ۰ (False) حساب می‌شوند.
"""

import csv
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

# جانشین‌های داخل CSV که پیش از رفتن به Word به نویسهٔ واقعی تبدیل می‌شوند.
# فرض: ^o همان نیم‌فاصله (ZWNJ) است. (نیاز به تأیید)
PLACEHOLDERS = {"^o": "\u200c"}

# هر گروه قاعده → فایل‌های آن (به ترتیب اولویت؛ در تعارض، ردیف اول برنده است)
RULE_GROUPS = {
    "half_space": ["HalfSpace1002.csv"],
    # نشانه‌گذاری = علائم نگارشی + تشدید + تنوین (فایل‌های ۱۰۰۰)
    "punctuation": ["Signs1000.csv", "Tashdid1000.csv", "Tanvin1000.csv"],
    "spelling": ["SpellingCorrection1001.csv"],
    "standard": ["Standard1004.csv"],
}

REQUIRED_COLUMNS = (
    "Search", "Replace", "Wildcard", "MatchCase", "MatchWholeWord",
    "MatchKashida", "MatchDiacritics", "MatchAlefHamza", "CounterUp",
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
    source: str   # نام فایل
    line: int     # شمارهٔ خط در فایل (برای گزارش خطا)


@dataclass
class RuleSet:
    rules: list = field(default_factory=list)
    skipped: list = field(default_factory=list)   # (فایل, خط, دلیل, Search)

    def summary(self):
        return f"{len(self.rules)} قاعدهٔ فعال، {len(self.skipped)} ردیف ردشده"


def _flag(value):
    return (value or "").strip() == "1"


def _expand(text):
    for token, char in PLACEHOLDERS.items():
        text = text.replace(token, char)
    return text


def _read_file(path: Path):
    if not path.exists():
        raise RuntimeError(f"فایل داده پیدا نشد:\n{path}")
    with path.open(encoding="utf-8-sig", newline="") as fh:   # utf-8-sig: حذف BOM
        reader = csv.DictReader(fh)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise RuntimeError(f"ستون‌های لازم در «{path.name}» نیست: {', '.join(missing)}")
        for row in reader:
            yield reader.line_num, row


_cache = {}


def load_group(group: str, data_dir: Path = None) -> RuleSet:
    """قواعد یک گروه را می‌خواند؛ نتیجه کش می‌شود (فقط یک‌بار خواندن از دیسک)."""
    if group not in RULE_GROUPS:
        raise RuntimeError(f"گروه قاعدهٔ ناشناخته: {group}")
    data_dir = Path(data_dir) if data_dir else DATA_DIR
    key = (group, str(data_dir))
    if key in _cache:
        return _cache[key]

    result = RuleSet()
    seen = {}   # Search → Replace نخستین

    for name in RULE_GROUPS[group]:
        for line, row in _read_file(data_dir / name):
            search = _expand(row["Search"] or "")
            replace = _expand(row["Replace"] or "")

            if search == "":                       # جداکنندهٔ بصری
                continue
            if search == replace:
                result.skipped.append((name, line, "بدون تغییر (Search = Replace)", search))
                continue
            if search in seen:
                reason = "تکراری" if seen[search] == replace else "تعارض با ردیف قبلی (نسخهٔ اول استفاده می‌شود)"
                result.skipped.append((name, line, reason, search))
                continue
            seen[search] = replace

            result.rules.append(Rule(
                search=search, replace=replace,
                wildcard=_flag(row["Wildcard"]),
                match_case=_flag(row["MatchCase"]),
                whole_word=_flag(row["MatchWholeWord"]),
                kashida=_flag(row["MatchKashida"]),
                diacritics=_flag(row["MatchDiacritics"]),
                alef_hamza=_flag(row["MatchAlefHamza"]),
                count=_flag(row["CounterUp"]),
                source=name, line=line,
            ))

    _cache[key] = result
    return result