"""لایهٔ امنیتی: شناسهٔ دستگاه و امضای HMAC اسناد."""

import hashlib
import hmac
import json

try:  # اجرا به‌صورت پکیج: python main.py از داخل article_negar_modular
    from .config import DEMO_SECRET
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.config import DEMO_SECRET

try:  # winreg فقط روی ویندوز وجود دارد؛ برای تست/ایمپورت روی سیستم‌های دیگر
    import winreg  # type: ignore
except ImportError:  # pragma: no cover - فقط برای محیط غیرویندوزی
    winreg = None


def get_device_guid():
    """دریافت شناسهٔ اختصاصی ویندوز برای قفل دستگاه."""
    if winreg is None:
        return "UNKNOWN_DEVICE_TOKEN"
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography"
        ) as key:
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            return hashlib.sha256(str(guid).encode()).hexdigest()
    except Exception:
        return "UNKNOWN_DEVICE_TOKEN"


def create_signature(data_dict: dict) -> str:
    """ساخت امضای HMAC-SHA256 برای دیکشنری داده."""
    encoded = json.dumps(
        data_dict, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hmac.new(DEMO_SECRET, encoded, hashlib.sha256).hexdigest()


def build_token(payload: dict) -> str:
    """ساخت رشتهٔ JSON شامل داده و امضای آن (برای ذخیره در Variables سند)."""
    token = {"payload": payload, "sig": create_signature(payload)}
    return json.dumps(token, ensure_ascii=False)


def verify_token(record: dict) -> dict:
    """اعتبارسنجی امضا و تعلق سند به این دستگاه؛ دیکشنری payload را برمی‌گرداند."""
    payload = record["payload"]
    sig = record["sig"]

    # ۱. یکپارچگی داده و دستکاری‌نشدن امضا
    if not hmac.compare_digest(create_signature(payload), sig):
        raise ValueError("امضای سند دستکاری شده و نامعتبر است!")

    # ۲. تعلق به این دستگاه
    if not hmac.compare_digest(payload.get("device_id", ""), get_device_guid()):
        raise ValueError("این سند روی سیستم دیگری لایسنس شده است!")

    return payload
