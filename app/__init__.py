"""بستهٔ ماژولار «مقاله‌نگار».

نکتهٔ مهم: در این نسخه هیچ ایمپورت سنگینی در بالای __init__ انجام نمی‌شود تا
خطای زنجیره‌ای ModuleNotFoundError رخ ندهد. دسترسی به کلاس‌ها به‌صورت
تنبل (lazy) و با __getattr__ انجام می‌شود؛ بنابراین هر دو حالت زیر کار می‌کنند:

    from app import LuxuryWordAssistant
    from app.ui import LuxuryWordAssistant
"""

from importlib import import_module

__all__ = ["LuxuryWordAssistant", "WordEngine", "DocumentActions"]
__version__ = "1.0.0"

_LAZY = {
    "LuxuryWordAssistant": "app.ui",
    "WordEngine": "app.word_engine",
    "DocumentActions": "app.actions_document",
}


def __getattr__(name):
    module_name = _LAZY.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY.keys()))
