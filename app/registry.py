"""رجیستری کارت‌های منو."""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

# ترتیب تب‌ها (تنها جایی که نام تب‌ها تعریف می‌شود)
TAB_NAMES = [
    "شیوانگار",
    "مقاله‌نگار",
    "یزدنگار",
    "ازادنگار",
    "مدیریت متن",
    "عنوان و ارجاع",
    "پانویس",
    "مدیریت منابع",
    "مدیریت سند",
    "ابزارها",
]


@dataclass(frozen=True)
class Card:
    tab: str
    title: str
    subtitle: str
    command: Optional[Callable]  # None => کارت غیرفعال (خاکستری)
    order: int = 100
    anchor: bool = False  # اگر True: command(app, card_widget)
    settings: Optional[Callable] = None  # دکمهٔ ↖ کارت: settings(app)


_CARDS: Dict[str, Dict[str, Card]] = {name: {} for name in TAB_NAMES}


def _add(new: Card) -> None:
    if new.tab not in _CARDS:
        raise ValueError(f"تب ناشناخته: {new.tab!r}")
    if new.title in _CARDS[new.tab]:
        raise ValueError(f"کارت تکراری در تب {new.tab!r}: {new.title!r}")
    _CARDS[new.tab][new.title] = new


def card(tab, title, subtitle="", *, order=100, anchor=False, settings=None):
    """دکوراتور: تابع fn(app) را به‌عنوان کارت فعال ثبت می‌کند."""

    def decorator(fn):
        _add(Card(tab, title, subtitle, fn, order, anchor, settings))
        return fn

    return decorator


def placeholder(tab, title, subtitle="", *, order=100):
    """کارت غیرفعال (خاکستری) تا زمانی که قابلیتش نوشته شود."""
    _add(Card(tab, title, subtitle, None, order))


def cards_for(tab: str) -> List[Card]:
    return sorted(_CARDS[tab].values(), key=lambda c: (c.order, c.title))