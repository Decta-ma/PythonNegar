
"""قالب‌بندی شعر در سند Word."""

from .config import (
    WD_ALIGN_PARAGRAPH_CENTER,
    WD_ALIGN_PARAGRAPH_RIGHT,
    WD_AUTO_FIT_WINDOW,
    WD_FIND_STOP,
    WD_REPLACE_ALL,
    WD_TABLE_DIRECTION_RTL,
)


def _get_paragraphs_in_range(doc, selected_range):
    """پیدا کردن پاراگراف‌های واقع در محدوده انتخاب‌شده."""

    selected_start = selected_range.Start
    selected_end = selected_range.End

    paragraphs = []

    for index in range(1, doc.Paragraphs.Count + 1):
        paragraph = doc.Paragraphs.Item(index)
        paragraph_range = paragraph.Range

        if (
            paragraph_range.Start < selected_end
            and paragraph_range.End > selected_start
        ):
            paragraphs.append(paragraph)

    return paragraphs



def _get_selected_poetry(engine, target_range=None):
    """دریافت و اعتبارسنجی مصراع‌های محدوده موردنظر."""

    doc = engine.ensure_ready()
    word = engine.word

    if target_range is None:
        selected_range = word.Selection.Range.Duplicate
    else:
        selected_range = target_range.Duplicate

    if selected_range.Start == selected_range.End:
        raise RuntimeError("هیچ متنی برای قالب‌بندی وجود ندارد.")

    selected_start = selected_range.Start
    selected_end = selected_range.End

    paragraphs = _get_paragraphs_in_range(doc, selected_range)

    if not paragraphs:
        raise RuntimeError("هیچ پاراگرافی در محدوده موردنظر پیدا نشد.")

    # بررسی شروع انتخاب از ابتدای پاراگراف
    first_range = paragraphs[0].Range

    if selected_start > first_range.Start:
        raise RuntimeError(
            "انتخاب شما باید از ابتدای اولین پاراگراف شروع شود."
        )

    texts = []

    for index, paragraph in enumerate(paragraphs, start=1):
        paragraph_range = paragraph.Range

        # حذف علامت پایان پاراگراف
        paragraph_text = paragraph_range.Text.rstrip("\r\n\x07")

        # هر شکست خط داخلی نیز یک مصراع جداگانه است.
        hemistichs = paragraph_text.split("\x0b")

        # بررسی کامل بودن پاراگراف‌های انتخاب‌شده
        if index < len(paragraphs):
            if selected_end < paragraph_range.End:
                raise RuntimeError(
                    "لطفاً پاراگراف‌ها را به‌صورت کامل انتخاب کنید."
                )
        elif selected_end < paragraph_range.End - 1:
            raise RuntimeError(
                "انتخاب شما آخرین مصراع را کامل پوشش نمی‌دهد."
            )

        for hemistich in hemistichs:
            if not hemistich.strip():
                raise RuntimeError(
                    f"مصراع شماره {len(texts) + 1} خالی است."
                )

            texts.append(hemistich)

    if len(texts) < 2:
        raise RuntimeError("حداقل دو مصراع باید وجود داشته باشد.")

    if len(texts) % 2 != 0:
        raise RuntimeError(
            f"تعداد مصراع‌های شناسایی‌شده {len(texts)} است "
            "و باید زوج باشد."
        )

    return doc, selected_range, paragraphs, texts




def _replace_manual_breaks(selected_range):
    """تبدیل شکست خط داخلی به پایان پاراگراف، بدون تغییر محدوده اصلی."""

    # تعداد شکست خط‌های داخلی قبل از جایگزینی
    original_text = selected_range.Text
    break_count = original_text.count("\x0b")

    # روی یک کپی کار می‌کنیم تا محدوده اصلی تغییر نکند
    find_range = selected_range.Duplicate
    find = find_range.Find

    find.Execute(
        FindText="^l",
        ReplaceWith="^p",
        Replace=WD_REPLACE_ALL,
        Forward=True,
        Wrap=WD_FIND_STOP,
    )

    # محدوده تازه را از روی موقعیت اولیه سند می‌سازیم
    doc = selected_range.Document

    return doc.Range(
        selected_range.Start,
        selected_range.End
    ), break_count



def _start_undo_record(word, title):
    """شروع یک عملیات یکپارچه برای Undo."""

    try:
        undo_record = word.UndoRecord
        undo_record.StartCustomRecord(title)
        return undo_record
    except Exception:
        return None


def format_poetry_single_column(engine,target_range=None):
    """قرار دادن دو مصراع هر بیت زیر یکدیگر."""

    doc, selected_range, old_paragraphs, texts = (
    _get_selected_poetry(engine, target_range)
   )

    word = engine.word
    old_screen_updating = word.ScreenUpdating
    undo_record = None

    try:
        word.ScreenUpdating = False

        undo_record = _start_undo_record(
            word, "قالب شعر - تک ستونه"
        )

        working_range, break_count = _replace_manual_breaks(selected_range)

        paragraphs = _get_paragraphs_in_range(doc, working_range)         

        if len(paragraphs) != len(texts):
            raise RuntimeError(
                "تعداد پاراگراف‌های ایجادشده با تعداد مصراع‌ها مطابقت ندارد."
            )

        for index, paragraph in enumerate(paragraphs, start=1):
            paragraph_format = paragraph.Format

            # تنظیم جهت و ترازبندی شعر
            paragraph_format.Alignment = WD_ALIGN_PARAGRAPH_RIGHT

            # جلوگیری از شکسته شدن مصراع در صفحات
            paragraph_format.KeepTogether = True

            # فاصله بین دو مصراع یک بیت
            if index % 2 == 1:
                paragraph_format.SpaceAfter = 0
            else:
                # فاصله بیشتر بین بیت‌ها
                paragraph_format.SpaceAfter = 12

        doc.Save()

        return (
            "قالب تک‌ستونه با موفقیت اعمال شد.\n"
            f"تعداد مصراع‌ها: {len(texts)}\n"
            f"تعداد بیت‌ها: {len(texts) // 2}"
        )

    finally:
        if undo_record is not None:
            try:
                undo_record.EndCustomRecord()
            except Exception:
                pass

        word.ScreenUpdating = old_screen_updating


def format_poetry_two_columns(engine,target_range=None):
    """قرار دادن دو مصراع هر بیت در دو ستون روبه‌روی هم."""

    doc, selected_range, old_paragraphs, texts = (
       _get_selected_poetry(engine, target_range)
    )

    word = engine.word
    old_screen_updating = word.ScreenUpdating
    undo_record = None

    try:
        word.ScreenUpdating = False

        undo_record = _start_undo_record(
            word, "قالب شعر - دو ستونه"
        )

        working_range, break_count = _replace_manual_breaks(selected_range)

        table = working_range.ConvertToTable(
          Separator=0,
          NumColumns=2,
          NumRows=len(texts) // 2,
          AutoFitBehavior=WD_AUTO_FIT_WINDOW,
         )

        # تنظیم جهت جدول برای زبان فارسی
        table.TableDirection = WD_TABLE_DIRECTION_RTL

        # حذف کادرهای جدول
        table.Borders.Enable = False

        # تنظیم عرض جدول متناسب با عرض صفحه
        table.AutoFitBehavior(WD_AUTO_FIT_WINDOW)

        # تنظیم سلول‌های هر بیت
        for row_index in range(1, table.Rows.Count + 1):
            row = table.Rows.Item(row_index)

            # جلوگیری از شکسته شدن یک بیت بین دو صفحه
            row.AllowBreakAcrossPages = False

            right_cell = row.Cells.Item(1)
            left_cell = row.Cells.Item(2)

            # وسط‌چین کردن متن هر دو سلول
            right_cell.Range.ParagraphFormat.Alignment = (
                WD_ALIGN_PARAGRAPH_CENTER
            )
            left_cell.Range.ParagraphFormat.Alignment = (
                WD_ALIGN_PARAGRAPH_CENTER
            )

            # وسط‌چین عمودی محتوا
            right_cell.VerticalAlignment = 1
            left_cell.VerticalAlignment = 1

        doc.Save()

        return (
            "قالب دو‌ستونه با موفقیت اعمال شد.\n"
            f"تعداد مصراع‌ها: {len(texts)}\n"
            f"تعداد بیت‌ها: {len(texts) // 2}"
        )

    finally:
        if undo_record is not None:
            try:
                undo_record.EndCustomRecord()
            except Exception:
                pass

        word.ScreenUpdating = old_screen_updating
