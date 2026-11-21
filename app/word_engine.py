"""هستهٔ ارتباط با مایکروسافت ورد: تمام متدهای WordEngine."""

import json
import uuid
from pathlib import Path

import pywintypes
import win32com.client

try:  # اجرا به‌صورت پکیج
    from .config import (
        VARIABLE_NAME,
        WD_COLOR_RED,
        WD_FIND_CONTINUE,
        WD_DOCX,
        WD_FIND_STOP,
        WD_REPLACE_ALL,
    )
    from .security import build_token, create_signature, get_device_guid, verify_token
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.config import (
        VARIABLE_NAME,
        WD_COLOR_RED,
        WD_FIND_CONTINUE,
        WD_DOCX,
        WD_FIND_STOP,
        WD_REPLACE_ALL,
    )
    from app.security import build_token, create_signature, get_device_guid, verify_token


class WordEngine:
    """رانندهٔ COM ورد همراه با سیستم امضای اسناد (مطابق home-(2).py)."""

    def __init__(self):
        self.word = None
        self.doc = None

    # ---------------------------------------------------------------- اتصال به ورد
    def get_word_app(self, start_if_missing=False):
        """اتصال به نمونهٔ فعال ورد یا اجرای نمونهٔ جدید."""
        if self.word is not None:
            try:
                _ = self.word.Documents.Count
                return self.word
            except Exception:
                self.word = None
                self.doc = None

        try:
            self.word = win32com.client.GetActiveObject("Word.Application")
        except pywintypes.com_error:
            if not start_if_missing:
                raise RuntimeError("هیچ برنامهٔ Word فعالی یافت نشد!") from None
            self.word = win32com.client.DispatchEx("Word.Application")

        self.word.Visible = True
        return self.word

    # ---------------------------------------------------------------- امضا
    def set_doc_signature(self, doc, file_name: str, doc_id: str = None):
        """تولید و ثبت امضای وابسته به نام فایل و شناسهٔ سیستم."""
        payload = {
            "doc_id": doc_id or uuid.uuid4().hex,
            "file_name": file_name,
            "device_id": get_device_guid(),
        }
        raw = build_token(payload)

        # اگر از قبل متغیر وجود داشت آپدیت شود، وگرنه اضافه شود
        try:
            doc.Variables(VARIABLE_NAME).Value = raw
        except pywintypes.com_error:
            doc.Variables.Add(Name=VARIABLE_NAME, Value=raw)

        return payload["doc_id"]

    def create_new_signed_doc(self, file_path: str, template_path=None):
        """ساخت سند جدید امضاشده و ذخیره با فرمت DOCX."""
        path = Path(file_path)
        if path.suffix.lower() != ".docx":
            path = path.with_suffix(".docx")
        if path.exists():
            raise RuntimeError("فایلی با این نام از قبل وجود دارد.")

        word = self.get_word_app(start_if_missing=True)
        if template_path:
            template_path = Path(template_path)
            print("Template path:", template_path)
            print("Template exists:", template_path.exists())
            print("Template extension:", template_path.suffix)

            if template_path.exists():
                import zipfile

                print("Is valid ZIP:", zipfile.is_zipfile(template_path))

                if zipfile.is_zipfile(template_path):
                    with zipfile.ZipFile(template_path, "r") as z:
                        print("ZIP test:", z.testzip())
            doc = word.Documents.Add(
                Template=str(template_path),
                NewTemplate=False
            )
        else:
            doc = word.Documents.Add()

        try:
            self.set_doc_signature(doc, path.name)
            doc.SaveAs2(FileName=str(path), FileFormat=WD_DOCX)
        except Exception:
            doc.Close(SaveChanges=0)
            raise

        self.doc = doc
        return doc.Name

    def verify_document(self, doc):
        """اعتبارسنجی کامل سند: امضا، دستگاه و تطابق نام فایل."""
        try:
            raw = doc.Variables(VARIABLE_NAME).Value
            record = json.loads(raw)
            payload = verify_token(record)

            # ۳. تطابق دقیق نام فایل (جلوگیری از Rename دستی یا کپی با نام دیگر)
            current_name = doc.Name
            licensed_name = payload.get("file_name", "")
            if current_name.lower() != licensed_name.lower():
                raise RuntimeError(
                    f"نام این فایل تغییر کرده یا کپی شده است!\n"
                    f"نام اصلی مجاز: {licensed_name}\n"
                    f"نام فایل فعلی: {current_name}\n\n"
                    f"برای تغییر نام، فقط از دکمه «تغییر نام رسمی سند» در برنامه استفاده کنید."
                )
            return payload

        except RuntimeError:
            raise
        except (pywintypes.com_error, KeyError, ValueError, TypeError) as exc:
            raise RuntimeError("این سند فاقد امضای معتبر این نرم‌افزار است.") from exc

    def connect_to_active(self):
        """اتصال به سند فعال ورد پس از تأیید امضا."""
        word = self.get_word_app(start_if_missing=False)
        if word.Documents.Count == 0:
            raise RuntimeError("هیچ فایلی در ورد باز نیست.")

        doc = word.ActiveDocument
        self.verify_document(doc)
        self.doc = doc
        return doc.Name

    def ensure_ready(self):
        """اطمینان از آماده‌بودن همان سند متصل‌شده و غیرفقط‌خواندنی بودن آن."""
        if not self.doc:
            raise RuntimeError("ابتدا به سند متصل شوید یا سند جدید بسازید.")
        word = self.get_word_app(start_if_missing=False)
        if word.ActiveDocument.FullName != self.doc.FullName:
            raise RuntimeError("سند فعال در ورد تغییر کرده است؛ دوباره متصل شوید.")
        if self.doc.ReadOnly:
            raise RuntimeError("سند در حالت فقط‌خواندنی (Read-Only) است.")
        return self.doc

    def rename_active_document(self, new_raw_name: str):
        """تغییر نام رسمی سند به همراه بازنویسی و به‌روزرسانی کلید امنیتی."""
        doc = self.ensure_ready()

        # پاکسازی و اعتبارسنجی نام جدید
        new_name = new_raw_name.strip()
        if not new_name:
            raise RuntimeError("نام فایل معتبر نیست.")
        if not new_name.lower().endswith(".docx"):
            new_name += ".docx"

        old_full_path = Path(doc.FullName)
        new_full_path = old_full_path.parent / new_name

        if old_full_path.name.lower() == new_name.lower():
            raise RuntimeError("نام جدید با نام فعلی فایل یکسان است.")

        if new_full_path.exists():
            raise RuntimeError("فایلی با این نام در این مسیر از قبل وجود دارد.")

        # استخراج doc_id قبلی برای تداوم سابقهٔ سند
        raw = doc.Variables(VARIABLE_NAME).Value
        record = json.loads(raw)
        doc_id = record["payload"].get("doc_id")

        # ثبت امضای جدید منطبق بر نام فایل جدید
        self.set_doc_signature(doc, file_name=new_name, doc_id=doc_id)

        # ذخیره سند تحت نام جدید
        doc.SaveAs2(FileName=str(new_full_path), FileFormat=WD_DOCX)

        # حذف فایل قدیمی تا نسخهٔ کپی نماند
        try:
            if old_full_path.exists():
                old_full_path.unlink()
        except Exception:
            pass  # اگر فایل توسط پروسه‌ای قفل بود نادیده گرفته می‌شود

        return doc.Name

    # ---------------------------------------------------------------- عملیات متنی
    def set_selection_red(self):
        """قرمز کردن متن انتخاب‌شده و ذخیرهٔ سند."""
        doc = self.ensure_ready()
        sel = self.word.Selection
        if sel.Range.Start == sel.Range.End:
            raise RuntimeError("لطفاً ابتدا متنی را در سند انتخاب کنید.")
        sel.Range.Font.Color = WD_COLOR_RED
        doc.Save()
        return "متن انتخاب‌شده به رنگ قرمز درآمد و ذخیره شد."

    def fix_extra_spaces(self):
        """حذف فاصله‌های اضافه و تکراری (اسپیس معمولی و نشکن) و ذخیرهٔ سند."""
        doc = self.ensure_ready()
        changed = False

        # الگوهای فاصله‌های اضافه (اسپیس معمولی و اسپیس‌های نشکن)
        patterns_to_fix = [
            ("  ", " "),
            ("\u00a0\u00a0", " "),
            (" \u00a0", " "),
            ("\u00a0 ", " "),
        ]

        for target, replacement in patterns_to_fix:
            for _ in range(15):
                rng = doc.Content
                finder = rng.Find
                finder.ClearFormatting()
                finder.Replacement.ClearFormatting()

                found = finder.Execute(
                    FindText=target,
                    MatchCase=False,
                    MatchWholeWord=False,
                    MatchWildcards=False,
                    Forward=True,
                    Wrap=WD_FIND_CONTINUE,
                    Format=False,
                    ReplaceWith=replacement,
                    Replace=WD_REPLACE_ALL,
                )
                if not found:
                    break
                changed = True

        if changed:
            doc.Save()
            return "تمام فاصله‌های اضافه و تکراری با موفقیت اصلاح و ذخیره شدند."
        return "هیچ فاصلهٔ اضافه‌ای در متن پیدا نشد."
