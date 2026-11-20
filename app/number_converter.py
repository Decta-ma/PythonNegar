
"""تبدیل اعداد فارسی، انگلیسی و عربی در سند Word."""

ENGLISH_DIGITS = "0123456789"
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"


def _build_translation_map(source_digits, target_digits):
    return {
        source: target
        for source, target in zip(source_digits, target_digits)
    }


def _replace_digits_in_range(rng, translation_map):
    """
    اعداد را در یک Range از انتها به ابتدا تبدیل می‌کند.

    تبدیل از انتها به ابتدا باعث می‌شود تغییر طول متن،
    موقعیت کاراکترهایی که هنوز بررسی نشده‌اند را خراب نکند.
    """

    changed_count = 0

    start = rng.Start
    end = rng.End

    for position in range(end - 1, start - 1, -1):
        char_range = rng.Duplicate
        char_range.Start = position
        char_range.End = position + 1

        char = char_range.Text

        if char in translation_map:
            char_range.Text = translation_map[char]
            changed_count += 1

    return changed_count


def _iter_story_ranges(doc):
    """تمام StoryRangeهای قابل دسترسی Word را پیمایش می‌کند."""

    for story_type in range(1, 18):
        try:
            rng = doc.StoryRanges(story_type)
        except Exception:
            continue

        while rng is not None:
            yield rng.Duplicate

            try:
                rng = rng.NextStoryRange
            except Exception:
                break


def _convert_document(doc, translation_map, target_range=None):
    """تبدیل اعداد در محدوده مشخص یا تمام بخش‌های سند."""

    total_changed = 0

    if target_range is not None:
        return _replace_digits_in_range(
            target_range,
            translation_map,
        )

    for rng in _iter_story_ranges(doc):
        total_changed += _replace_digits_in_range(
            rng,
            translation_map,
        )

    return total_changed


def convert_document_to_persian(doc, target_range=None):
    """تبدیل اعداد انگلیسی و عربی به اعداد فارسی."""

    translation_map = {}

    translation_map.update(
        _build_translation_map(
            ENGLISH_DIGITS,
            PERSIAN_DIGITS,
        )
    )

    translation_map.update(
        _build_translation_map(
            ARABIC_DIGITS,
            PERSIAN_DIGITS,
        )
    )

    return _convert_document(
        doc,
        translation_map,
        target_range,
    )


def convert_document_to_english(doc, target_range=None):
    """تبدیل اعداد فارسی و عربی به اعداد انگلیسی."""

    translation_map = {}

    translation_map.update(
        _build_translation_map(
            PERSIAN_DIGITS,
            ENGLISH_DIGITS,
        )
    )

    translation_map.update(
        _build_translation_map(
            ARABIC_DIGITS,
            ENGLISH_DIGITS,
        )
    )

    return _convert_document(
        doc,
        translation_map,
        target_range,
    )
