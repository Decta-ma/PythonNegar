"""رابط کاربری گرافیکی مدرن و لوکس (CustomTkinter)."""

try:  # اجرا به‌صورت پکیج
    from . import features, registry, theme
    from .word_engine import WordEngine
    from .actions_equation import EquationActions
    from .actions_document import DocumentActions
    from .actions_editing import EditingActions
    from .actions_figure import FigureActions
    from .actions_table import TableActions
    from .actions_footnote import FootnoteActions
    from .ui_components.settings_btn import settings_btn
    
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app import features, registry, theme
    from app.config import *  # noqa: F401,F403
    from app.word_engine import WordEngine
    from app.actions_document import DocumentActions
    from app.actions_table import TableActions
    from app.actions_editing import EditingActions
    from app.actions_figure import FigureActions
    from app.actions_footnote import FootnoteActions
    from app.actions_equation import EquationActions
    from app.ui_components.settings_btn import settings_btn

import traceback
import customtkinter as ctk
import pythoncom

# ثبت همهٔ کارت‌ها (هر فایل در app/features/ خودش را ثبت می‌کند)
features.load_all()

class LuxuryWordAssistant(
    DocumentActions,
    EquationActions,
    FigureActions,
    TableActions,
    ctk.CTk,
    EditingActions,
    FootnoteActions,
):
    def __init__(self):
        super().__init__()
        pythoncom.CoInitialize()
        self.engine = WordEngine()

        # تنظیمات پنجره
        self.title("دستیار هوشمند ورد | نگارش دانشگاهی")
        self.geometry("380x610")
        self.resizable(False, False)
        # self.attributes("-topmost", True)  # همیشه شناور روی ورد

        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0A1124")

        self._status_after_id = None
        self._status_connected = False
        self.setup_ui()

    # ------------------------------------------------------------------ ساخت رابط
    def setup_ui(self):
        # پنجرهٔ اصلی
        self.geometry("900x610")
        self.minsize(760, 560)

        # رنگ‌های رابط
        self.bg = theme.BG
        self.panel = theme.PANEL
        self.panel_light = theme.PANEL_LIGHT
        self.blue = theme.BLUE
        self.blue_hover = theme.BLUE_HOVER
        self.text = theme.TEXT
        self.muted = theme.MUTED
        self.line = theme.LINE

        # قاب اصلی
        root = ctk.CTkFrame(self, fg_color=self.bg, corner_radius=0)
        root.pack(fill="both", expand=True)

        # سربرگ
        header = ctk.CTkFrame(root, fg_color=self.panel, corner_radius=14)
        header.pack(fill="x", padx=18, pady=(16, 10))

        ctk.CTkLabel(
            header,
            text="مقاله‌نگار",
            font=ctk.CTkFont(family="Vazirmatn", size=22, weight="bold"),
            text_color=self.text,
        ).pack(anchor="e", padx=18, pady=(12, 2))

        ctk.CTkLabel(
            header,
            text="دستیار قالب‌بندی و نگارش اسناد دانشگاهی",
            font=ctk.CTkFont(family="Vazirmatn", size=12),
            text_color="#93C5FD",
        ).pack(anchor="e", padx=18, pady=(0, 12))

        # نوار تب‌های اصلی
        self.tabs_frame = ctk.CTkFrame(root, fg_color=self.panel, corner_radius=12)
        self.tabs_frame.pack(fill="x", padx=18, pady=(0, 10))

        self.tab_names = list(registry.TAB_NAMES)
        self.tab_buttons = {}

        for tab_name in self.tab_names:
            button = ctk.CTkButton(
                self.tabs_frame,
                text=tab_name,
                width=112,
                height=42,
                corner_radius=9,
                font=ctk.CTkFont(family="Vazirmatn", size=12, weight="bold"),
                fg_color=self.blue if tab_name == "مقاله‌نگار" else "transparent",
                hover_color=self.blue_hover,
                text_color=self.text,
                command=lambda name=tab_name: self.show_tab(name),
            )
            button.pack(side="right", padx=4, pady=7)
            self.tab_buttons[tab_name] = button

        # ناحیهٔ زیرشاخه‌ها
        self.content = ctk.CTkFrame(
            root,
            fg_color=self.panel,
            corner_radius=14,
            border_width=1,
            border_color=self.line,
        )
        self.content.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        # فوتر (به‌همراه چراغ و متن وضعیت)
        footer = ctk.CTkFrame(root, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(0, 10))

        self.status_dot = ctk.CTkLabel(
            footer, text="\u25cf", font=ctk.CTkFont(size=14), text_color="#64748B"
        )
        self.status_dot.pack(side="left", padx=(0, 8))

        self.status_text = ctk.CTkLabel(
            footer,
            text="آمادهٔ کار — ابتدا سند بسازید یا به سند باز ورد متصل شوید",
            font=ctk.CTkFont(family="Vazirmatn", size=10),
            text_color=self.muted,
        )
        self.status_text.pack(side="left")

        ctk.CTkLabel(
            footer,
            text="نسخهٔ نمایشی رابط کاربری — امضای اسناد فعال است",
            font=ctk.CTkFont(family="Vazirmatn", size=10),
            text_color=self.muted,
        ).pack(anchor="e")

        self.show_tab("مقاله‌نگار")
        self.update_status("وضعیت: سندی متصل نیست", is_connected=False)

    # ------------------------------------------------------------ وضعیت اتصال
    def update_status(self, text, is_connected=True, doc_name=None):
        """نمایش وضعیت سند و مدیریت چراغ اتصال."""
        if self._status_after_id is not None:
            try:
                self.after_cancel(self._status_after_id)
            except Exception:
                pass
            self._status_after_id = None

        self._status_connected = bool(is_connected)
        if self._status_connected:
            label = f"وضعیت: متصل به {doc_name}" if doc_name else text
            self.status_text.configure(text=label)
            self._status_led_bright = True
            self.status_dot.configure(text_color="#10B981")
            self._pulse_status_led()
        else:
            self.status_text.configure(text=text or "وضعیت: سندی متصل نیست")
            self.status_dot.configure(text_color="#64748B")

    def _pulse_status_led(self):
        if not self._status_connected or not self.status_dot.winfo_exists():
            return
        self._status_led_bright = not self._status_led_bright
        color = "#22C55E" if self._status_led_bright else "#065F46"
        self.status_dot.configure(text_color=color)
        self._status_after_id = self.after(700, self._pulse_status_led)

    # ------------------------------------------------------------------ تب‌ها
    def show_tab(self, tab_name):
        # نمایش تب انتخاب‌شده
        for name, button in self.tab_buttons.items():
            button.configure(fg_color=self.blue if name == tab_name else "transparent")

        # پاک‌کردن زیرشاخه‌های تب قبلی
        for widget in self.content.winfo_children():
            widget.destroy()

        # عنوان بخش
        ctk.CTkLabel(
            self.content,
            text=tab_name,
            font=ctk.CTkFont(family="Vazirmatn", size=17, weight="bold"),
            text_color="#60A5FA",
        ).pack(anchor="e", padx=20, pady=(18, 10))

        # کارت‌های گزینه‌ها
        cards = ctk.CTkFrame(self.content, fg_color="transparent")
        cards.pack(fill="both", expand=True, padx=12, pady=8)
        self.card_widgets = {}
        for index, item in enumerate(registry.cards_for(tab_name)):
            title, subtitle = item.title, item.subtitle
            active = item.command is not None
            card_bg = self.panel_light if active else theme.DISABLED_BG
            accent = theme.ACTIVE_ACCENT if active else theme.DISABLED_ACCENT
            subtitle_color = theme.ACTIVE_SUBTITLE if active else theme.DISABLED_ACCENT
            card = ctk.CTkFrame(
                cards,
                fg_color=card_bg,
                corner_radius=12,
                border_width=1,
                border_color=theme.ACTIVE_ACCENT if active else theme.DISABLED_BORDER,                height=96,
            )
            card.grid(
                row=index // 3,
                column=2 - (index % 3),
                padx=8,
                pady=8,
                sticky="nsew",
            )
            card.grid_propagate(False)
            self.card_widgets[title] = card

            ctk.CTkLabel(
                card,
                text="\u25a6",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=accent,
            ).pack(anchor="e", padx=12, pady=(10, 0))

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(family="Vazirmatn", size=13, weight="bold"),
                text_color=accent,
            ).pack(anchor="e", padx=12, pady=(2, 0))

            ctk.CTkLabel(
                card,
                text=subtitle,
                font=ctk.CTkFont(family="Vazirmatn", size=10),
                text_color=subtitle_color,
                wraplength=210,
                justify="right",
            ).pack(anchor="e", padx=12, pady=(2, 8))

            card.configure(cursor="hand2" if active else "arrow")
            if active:
                invoke = lambda event, item=item: self._run_card(item)
                card.bind("<Button-1>", invoke)
                for child in card.winfo_children():
                    child.configure(cursor="hand2")
                    child.bind("<Button-1>", invoke)
            else:
                for child in card.winfo_children():
                    child.configure(cursor="arrow")

            # دکمهٔ تنظیمات اختصاصی کارت (اگر فیچر settings داده باشد)
            if item.settings is not None:
                settings_btn(
                    card,
                    self.blue,
                    self.blue_hover,
                    self.text,
                    lambda item=item: item.settings(self),
                )
        # سه ستون با اندازهٔ یکسان
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1)

        # ------------------------------------------------------------
    # ------------------------------------------------------------ اجرای کارت
    def _run_card(self, item):
        """اجرای فرمان کارت؛ خطای یک فیچر کل برنامه را نمی‌بندد."""
        try:
            if item.anchor:
                item.command(self, self.card_widgets[item.title])
            else:
                item.command(self)
        except Exception:
            traceback.print_exc()
            self.update_status(f"خطا در اجرای «{item.title}»", is_connected=False)
