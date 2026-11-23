"""اعمال قواعد Find & Replace روی سند Word (مشترک بین همهٔ آیتم‌های ویراستاری).

این ماژول به WordEngine دست نمی‌زند؛ فقط از `engine.ensure_ready()` و `engine.word`
استفاده می‌کند، پس هر آیتم ویراستاری با یک خط به آن وصل می‌شود.
"""

from dataclasses import dataclass, field

# ثابت‌های Word (wdFindWrap / wdReplace / wdCollapseDirection)
WD_FIND_STOP = 0
WD_REPLACE_ALL = 2
WD_COLLAPSE_END = 0

MAX_PER_RULE = 100_000   # سقف ایمنی برای جلوگیری از حلقهٔ بی‌پایان


@dataclass
class ReplaceReport:
    total: int = 0                                  # کل جایگزینی‌های شمارش‌شده
    rules_run: int = 0                              # تعداد قواعد بررسی‌شده
    details: list = field(default_factory=list)     # [(rule, count)] فقط قواعد مؤثر

    def message(self, title):
        if self.total == 0:
            return f"«{title}»: موردی برای اصلاح پیدا نشد."
        return (f"«{title}» انجام شد.\n"
                f"{self.total} جایگزینی با {len(self.details)} قاعده انجام و سند ذخیره شد.")


def _find_args(rule):
    """آرگومان‌های Find.Execute مطابق ستون‌های CSV."""
    return dict(
        FindText=rule.search,
        MatchCase=rule.match_case,
        MatchWholeWord=rule.whole_word,
        MatchWildcards=rule.wildcard,
        MatchSoundsLike=False,
        MatchAllWordForms=False,
        Forward=True,
        Wrap=WD_FIND_STOP,
        Format=False,
        MatchKashida=rule.kashida,
        MatchDiacritics=rule.diacritics,
        MatchAlefHamza=rule.alef_hamza,
    )


def _count_matches(doc, rule, target_range=None):
    """شمارش مواردی که قاعده پیدا می‌کند."""

    rng = (
        target_range.Duplicate
        if target_range is not None
        else doc.Content.Duplicate
    )

    rng.Find.ClearFormatting()

    end = rng.End
    count = 0

    while count < MAX_PER_RULE:
        if not rng.Find.Execute(**_find_args(rule)):
            break

        count += 1

        rng.Collapse(WD_COLLAPSE_END)

        if rng.Start >= end:
            break

        rng.End = end

    return count


def _replace_all(doc, rule, target_range=None):
    """جایگزینی همه موارد در محدوده مشخص یا کل سند."""

    rng = (
        target_range.Duplicate
        if target_range is not None
        else doc.Content.Duplicate
    )

    rng.Find.ClearFormatting()
    rng.Find.Replacement.ClearFormatting()

    rng.Find.Execute(
        **_find_args(rule),
        ReplaceWith=rule.replace,
        Replace=WD_REPLACE_ALL,
    )


def apply_rules(
    engine,
    rules,
    undo_name="ویراستاری",
    progress=None,
    save=True,
    target_range=None,
):
    """قواعد را به ترتیب روی سند متصل اعمال می‌کند و ReplaceReport برمی‌گرداند.

    progress(done, total): پس از هر قاعده صدا زده می‌شود (برای نوار وضعیت).
    """
    doc = engine.ensure_ready()
    word = engine.word
    report = ReplaceReport()
    total_rules = len(rules)
    if total_rules == 0:
        return report

    # همهٔ تغییرات یک مرحلهٔ Undo شوند
    undo = None
    try:
        undo = word.UndoRecord
        undo.StartCustomRecord(undo_name)
    except Exception:
        undo = None

    # خاموش‌کردن بازتولید صفحه، سرعت را چند برابر می‌کند
    old_updating = None
    try:
        old_updating = word.ScreenUpdating
        word.ScreenUpdating = False
    except Exception:
        old_updating = None

    current = None
    
    try:
        for index, rule in enumerate(rules, start=1):
            current = rule

            matches = _count_matches(
                doc,
                rule,
                target_range,
            )

            if matches:
                _replace_all(
                    doc,
                    rule,
                    target_range,
                )

                report.total += matches
                report.details.append((rule, matches))

            report.rules_run = index

            if progress:
                progress(index, total_rules)

        if report.total > 0 and save:
            doc.Save()
            
    except Exception as exc:
        where = f"«{current.search.strip()}»" if current is not None else ""
        raise RuntimeError(f"خطا هنگام اعمال قاعدهٔ {where}:\n{exc}") from exc
    finally:
        if old_updating is not None:
            try:
                word.ScreenUpdating = old_updating
            except Exception:
                pass
        if undo is not None:
            try:
                undo.EndCustomRecord()
            except Exception:
                pass

    return report