"""تعویض خودکار زبان کیبورد ویندوز (فارسی / انگلیسی)."""

import ctypes
import sys

_LAYOUTS = {"fa": "00000429", "en": "00000409"}

_KLF_ACTIVATE = 0x00000001
_WM_INPUTLANGCHANGEREQUEST = 0x0050


def switch_layout(lang):
    """lang برابر "fa" یا "en". خارج از ویندوز یا در صورت خطا، بی‌صدا رد می‌شود."""
    if sys.platform != "win32":
        return
    try:
        user32 = ctypes.windll.user32
        user32.LoadKeyboardLayoutW.restype = ctypes.c_void_p
        user32.PostMessageW.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_size_t,
            ctypes.c_void_p,
        ]
        hkl = user32.LoadKeyboardLayoutW(_LAYOUTS[lang], _KLF_ACTIVATE)
        hwnd = user32.GetForegroundWindow()
        user32.PostMessageW(hwnd, _WM_INPUTLANGCHANGEREQUEST, 0, hkl)
    except Exception:
        pass