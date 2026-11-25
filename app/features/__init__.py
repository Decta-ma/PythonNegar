"""بارگذاری خودکار همهٔ ماژول‌های app/features (به‌جز فایل‌های شروع‌شده با _)."""

import importlib
import pkgutil
import traceback


def load_all():
    """همهٔ فیچرها را import می‌کند؛ خطا در یکی بقیه را از کار نمی‌اندازد."""
    failed = []
    for info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if info.name.startswith("_"):
            continue
        try:
            importlib.import_module(f"{__name__}.{info.name}")
        except Exception:
            failed.append(info.name)
            traceback.print_exc()
    return failed