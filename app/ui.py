"""رابط کاربری گرافیکی مدرن و لوکس (CustomTkinter)."""

try:  # اجرا به‌صورت پکیج
    from .config import *  # noqa: F401,F403
    from .word_engine import WordEngine
    from .actions_document import DocumentActions
    from .actions_editing import EditingActions
    from .actions_footnote import FootnoteActions
except ImportError:  # اجرا به‌صورت اسکریپت مستقل
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.config import *  # noqa: F401,F403
    from app.word_engine import WordEngine
    from app.actions_document import DocumentActions
    from app.actions_editing import EditingActions
    from app.actions_footnote import FootnoteActions

import customtkinter as ctk
import pythoncom

MENU_ITEMS = {
    "مقاله‌نگار": [
        ("قالب پایان‌نامه", "تنظیم ساختار پایان‌نامه", 0),
        ("قالب مقاله", "تنظیم ساختار مقاله", 0),
        ("قالب گزارش", "تنظیم ساختار گزارش", 0),
    ],
    "مدیریت متن": [
        ("استانداردسازی واژه‌ها", "یکسان‌سازی واژگان فارسی", 0),
        ("تنظیم پاراگراف", "فاصله، تورفتگی و چینش", 0),
        ("قالب‌بندی متن", "فونت، اندازه و سبک نوشتار", 0),
    ],
    "عنوان و ارجاع": [
        ("عنوان‌ها", "درج و قالب‌بندی عنوان‌ها", 0),
        ("فهرست مطالب", "مدیریت فهرست خودکار", 0),
        ("شکل و جدول", "عنوان‌گذاری و شماره‌گذاری", 0),
        ("ارجاع درون‌متنی", "درج ارجاع به بخش‌های سند", 0),
    ],
    "پانویس": [
        ("درج پانویس(پاورقی)", "افزودن پانویس به سند", 1),
        ("مدیریت پانویس‌ها", "مشاهده و تنظیم پانویس‌ها", 0),
        ("قالب پانویس", "تنظیم قلم و فاصله", 0),
    ],
    "مدیریت منابع": [
        ("افزودن منبع", "ثبت اطلاعات منبع", 0),
        ("کتاب‌نامه", "ساخت فهرست منابع", 0),
        ("سبک ارجاع‌دهی", "تنظیم شیوهٔ استناد", 0),
        ("به‌روزرسانی منابع", "بازسازی ارجاعات سند", 0),
    ],
    "مدیریت سند": [
        ("ساخت سند جدید", "ایجاد سند دانشگاهی", 1),
        ("اتصال به سند باز", "اتصال به سند فعال Word", 1),
        ("تغییر نام سند", "تغییر نام از داخل برنامه", 1),
        ("وضعیت سند", "نمایش اطلاعات و وضعیت سند", 0),
        ("ذخیرهٔ نسخه", "مدیریت نسخه‌های سند", 0),
        ("ویراستاری", "ویرایش سند", 1),
    ],
    "ابزارها": [
        ("تنظیمات", "تنظیمات برنامه", 0),
        ("راهنما", "راهنمای استفاده", 0),
        ("دربارهٔ برنامه", "اطلاعات نسخه", 0),
    ],
}


class LuxuryWordAssistant(
    DocumentActions,
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
        self.bg = "#0A1124"
        self.panel = "#101D3F"
        self.panel_light = "#14244D"
        self.blue = "#2563EB"
        self.blue_hover = "#3B82F6"
        self.text = "#F8FAFC"
        self.muted = "#94A3B8"
        self.line = "#23345B"

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

        self.tab_names = [
            "مقاله‌نگار",
            "مدیریت متن",
            "عنوان و ارجاع",
            "پانویس",
            "مدیریت منابع",
            "مدیریت سند",
            "ابزارها",
        ]
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

        commands = {
            "ساخت سند جدید": self.create_doc_action,
            "اتصال به سند باز": self.connect_doc_action,
            "تغییر نام سند": self.rename_doc_action,
            "ویراستاری": lambda: self.editing_menu_action(
                self.card_widgets["ویراستاری"]
            ),
            "درج پانویس(پاورقی)": lambda: self.footnote_menu_action(
                self.card_widgets["درج پانویس(پاورقی)"]
            ),
        }

        for index, (title, subtitle, enabled) in enumerate(MENU_ITEMS[tab_name]):
            active = enabled == 1
            card_bg = self.panel_light if active else "#1E293B"
            accent = "#39FF88" if active else "#64748B"
            subtitle_color = "#A7F3D0" if active else "#64748B"
            card = ctk.CTkFrame(
                cards,
                fg_color=card_bg,
                corner_radius=12,
                border_width=1,
                border_color="#39FF88" if active else "#475569",
                height=96,
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

            command = commands.get(title) if active else None
            card.configure(cursor="hand2" if command else "arrow")
            if command:
                handler = command
                invoke = lambda event, action=handler: action()
                card.bind("<Button-1>", invoke)
                for child in card.winfo_children():
                    child.configure(cursor="hand2")
                    child.bind("<Button-1>", invoke)
            else:
                for child in card.winfo_children():
                    child.configure(cursor="arrow")

                    # دکمه تنظیمات اختصاصی کارت ویراستاری
                    # دکمه تنظیمات اختصاصی کارت ویراستاری
            if title == "ویراستاری":
                settings_button = ctk.CTkButton(
                    card,
                    text="↖",
                    width=12,
                    height=10,
                    corner_radius=999,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    fg_color=self.blue,
                    hover_color=self.blue_hover,
                    text_color=self.text,
                    command=self.show_editing_settings_modal,
                )

                settings_button.place(
                    relx=0,
                    rely=1,
                    x=12,
                    y=-10,
                    anchor="sw",
                )

            # دکمه تنظیمات اختصاصی کارت پانویس
            if title == "درج پانویس(پاورقی)":
                settings_button = ctk.CTkButton(
                    card,
                    text="↖",
                    width=12,
                    height=10,
                    corner_radius=999,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    fg_color=self.blue,
                    hover_color=self.blue_hover,
                    text_color=self.text,
                    command=self.show_footnote_settings_modal,
                )

                settings_button.place(
                    relx=0,
                    rely=1,
                    x=12,
                    y=-10,
                    anchor="sw",
                )

        # سه ستون با اندازهٔ یکسان
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1)

        # ------------------------------------------------------------

    # تنظیمات ویراستاری
    # ------------------------------------------------------------

    def _add_settings_switch(self, parent, text, key, default=False):
        """ساخت یک گزینه روشن/خاموش در تنظیمات."""

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=42,
        )
        row.pack(fill="x", padx=8, pady=2)
        row.pack_propagate(False)

        label = ctk.CTkLabel(
            row,
            text=text,
            font=ctk.CTkFont(family="Vazirmatn", size=11),
            text_color=self.text,
            anchor="e",
        )
        label.pack(side="right", fill="both", expand=True, padx=8)

        switch = ctk.CTkSwitch(
            row,
            text="",
            width=42,
            progress_color=self.blue,
            button_color="#F8FAFC",
            button_hover_color="#CBD5E1",
            fg_color=self.line,
            onvalue=True,
            offvalue=False,
        )
        switch.pack(side="left", padx=8)

        if default:
            switch.select()
        else:
            switch.deselect()

        self.editing_settings_controls[key] = switch

        return switch

    def show_editing_settings_modal(self):
        """نمایش پنجره تنظیمات ویراستاری."""

        # جلوگیری از باز شدن چند پنجره هم‌زمان
        if (
            hasattr(self, "editing_settings_window")
            and self.editing_settings_window
            and self.editing_settings_window.winfo_exists()
        ):
            self.editing_settings_window.lift()
            return

        modal = ctk.CTkToplevel(self)
        self.editing_settings_window = modal

        modal.title("تنظیمات ویراستاری")
        modal.geometry("460x590")
        modal.resizable(False, False)
        modal.configure(fg_color=self.bg)

        modal.transient(self)
        modal.grab_set()

        # قرار گرفتن پنجره در مرکز برنامه
        self.update_idletasks()

        x = self.winfo_rootx() + (self.winfo_width() - 460) // 2

        y = self.winfo_rooty() + (self.winfo_height() - 590) // 2

        modal.geometry(f"460x590+{x}+{y}")

        # نگهداری کنترل‌های تنظیمات
        self.editing_settings_controls = {}

        # قاب اصلی
        main = ctk.CTkFrame(
            modal,
            fg_color=self.panel,
            corner_radius=16,
            border_width=1,
            border_color=self.line,
        )
        main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        # --------------------------------------------------
        # سربرگ
        # --------------------------------------------------

        header = ctk.CTkFrame(
            main,
            fg_color="transparent",
        )
        header.pack(fill="x", padx=16, pady=(12, 8))

        ctk.CTkButton(
            header,
            text="×",
            width=32,
            height=32,
            corner_radius=9,
            font=ctk.CTkFont(size=22),
            fg_color="transparent",
            hover_color=self.panel_light,
            text_color=self.muted,
            command=modal.destroy,
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="تنظیمات ویراستاری",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=17,
                weight="bold",
            ),
            text_color=self.text,
        ).pack(side="right")

        # خط جداکننده
        ctk.CTkFrame(
            main,
            height=2,
            fg_color=self.blue,
        ).pack(fill="x", padx=16, pady=(0, 12))

        # --------------------------------------------------
        # بخش ویراستار
        # --------------------------------------------------

        ctk.CTkLabel(
            main,
            text="ویراستار",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=12,
                weight="bold",
            ),
            text_color=self.blue_hover,
        ).pack(anchor="e", padx=20, pady=(4, 8))

        self._add_settings_switch(
            main,
            "اصلاح نیم‌فاصله در پانویس‌ها",
            "footnotes",
        )

        self._add_settings_switch(
            main,
            "اصلاح نیم‌فاصله در سرصفحه و پاصفحه",
            "headers_footers",
        )

        self._add_settings_switch(
            main,
            "اصلاح نیم‌فاصله در فیلدهای خاص",
            "special_fields",
        )

        self._add_settings_switch(
            main,
            "ویرایش‌های نشانه‌گذاری‌شده به کاربر نمایش داده شود",
            "show_revisions",
            default=True,
        )

        # --------------------------------------------------
        # بخش تبدیل اعداد
        # --------------------------------------------------

        ctk.CTkFrame(
            main,
            height=2,
            fg_color=self.line,
        ).pack(fill="x", padx=16, pady=(14, 10))

        ctk.CTkLabel(
            main,
            text="تبدیل اعداد",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=12,
                weight="bold",
            ),
            text_color=self.blue_hover,
        ).pack(anchor="e", padx=20, pady=(2, 8))

        self._add_settings_switch(
            main,
            "جایگزین کردن کاراکتر عدد",
            "replace_number_character",
        )

        # --------------------------------------------------
        # بخش شعر
        # --------------------------------------------------

        ctk.CTkFrame(
            main,
            height=2,
            fg_color=self.line,
        ).pack(fill="x", padx=16, pady=(14, 10))

        ctk.CTkLabel(
            main,
            text="شعر",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=12,
                weight="bold",
            ),
            text_color=self.blue_hover,
        ).pack(anchor="e", padx=20, pady=(2, 8))

        poetry_frame = ctk.CTkFrame(
            main,
            fg_color="transparent",
        )
        poetry_frame.pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            poetry_frame,
            text="شیوه نوشتن شعر",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=11,
            ),
            text_color=self.muted,
        ).pack(anchor="e", pady=(0, 8))

        poetry_menu = ctk.CTkOptionMenu(
            poetry_frame,
            values=[
                "به صورت ستونی",
                "به صورت دو ستونی",
            ],
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=11,
            ),
            fg_color=self.panel_light,
            button_color=self.blue,
            button_hover_color=self.blue_hover,
            text_color=self.text,
            dropdown_fg_color=self.panel,
            dropdown_hover_color=self.panel_light,
            dropdown_text_color=self.text,
            dynamic_resizing=False,
        )

        poetry_menu.set("به صورت ستونی")
        poetry_menu.pack(fill="x")

        self.editing_settings_controls["poetry_style"] = poetry_menu
    
    
    def show_footnote_settings_modal(self):
        """نمایش پنجره تنظیمات درج پانویس."""

        # جلوگیری از باز شدن چند پنجره هم‌زمان
        if (
            hasattr(self, "footnote_settings_window")
            and self.footnote_settings_window
            and self.footnote_settings_window.winfo_exists()
        ):
            self.footnote_settings_window.focus()
            return

        # تنظیمات پیش‌فرض
        if not hasattr(self, "footnote_settings"):
            self.footnote_settings = {}

        defaults = {
            "auto_keyboard": True,
            "auto_direction": True,
            "default_language": "فارسی",
            "display_mode": "معمولی",
            "separator_position": "چپ",
            "reference_style": "پیش‌فرض",
        }

        for key, value in defaults.items():
            self.footnote_settings.setdefault(key, value)

        settings = self.footnote_settings

        # ساخت پنجره
        window = ctk.CTkToplevel(self)
        self.footnote_settings_window = window

        window.title("تنظیمات پانویس")
        window.geometry("440x620")
        window.resizable(False, False)
        window.configure(fg_color=self.bg)
        window.transient(self)
        window.grab_set()

        window.update_idletasks()

        x = self.winfo_rootx() + (self.winfo_width() - 440) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 620) // 2
        window.geometry(f"440x620+{x}+{y}")

        def close_window():
            window.destroy()
            self.footnote_settings_window = None

        window.protocol("WM_DELETE_WINDOW", close_window)

        # پنل اصلی
        panel = ctk.CTkFrame(
            window,
            fg_color=self.panel,
            corner_radius=16,
            border_width=1,
            border_color=self.line,
        )
        panel.pack(fill="both", expand=True, padx=14, pady=14)

        # سربرگ
        header = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )
        header.pack(fill="x", padx=18, pady=(16, 10))

        close_button = ctk.CTkButton(
            header,
            text="✕",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=self.line,
            text_color=self.muted,
            command=close_window,
        )
        close_button.pack(side="left")

        title = ctk.CTkLabel(
            header,
            text="تنظیمات پانویس",
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=16,
                weight="bold",
            ),
            text_color=self.text,
        )
        title.pack(side="right")

        ctk.CTkFrame(
            panel,
            height=2,
            fg_color=self.blue,
        ).pack(fill="x", padx=18, pady=(0, 14))

        # نگهداری کنترل‌های تنظیمات
        controls = {}

        def add_option_row(title, key, options):
            """ساخت یک ردیف تنظیمات کشویی."""

            row = ctk.CTkFrame(
                panel,
                fg_color="transparent",
                height=62,
            )
            row.pack(fill="x", padx=20, pady=8)
            row.pack_propagate(False)

            option_menu = ctk.CTkOptionMenu(
                row,
                values=options,
                width=180,
                height=48,
                corner_radius=8,
                fg_color=self.panel_light,
                button_color=self.panel_light,
                button_hover_color=self.blue,
                dropdown_fg_color=self.panel,
                dropdown_hover_color=self.panel_light,
                text_color=self.text,
                font=ctk.CTkFont(
                    family="Vazirmatn",
                    size=11,
                ),
                dropdown_font=ctk.CTkFont(
                    family="Vazirmatn",
                    size=11,
                ),
            )

            current_value = settings.get(key, options[0])

            if current_value not in options:
                current_value = options[0]

            option_menu.set(current_value)
            option_menu.pack(side="left", padx=10)

            label = ctk.CTkLabel(
                row,
                text=title,
                font=ctk.CTkFont(
                    family="Vazirmatn",
                    size=11,
                ),
                text_color=self.text,
            )
            label.pack(side="right", padx=8)

            controls[key] = option_menu

        # نحوه نمایش پانویس
        add_option_row(
            "نحوه نمایش پانویس",
            "display_mode",
            [
                "معمولی",
                "دو ستونه",
            ],
        )

        # وضعیت خط جداکننده
        add_option_row(
            "وضعیت خط جداکننده پانویس",
            "separator_position",
            [
                "چپ",
                "راست",
                "وسط",
                "ممتد",
            ],
        )

        # شیوه ارجاع
        add_option_row(
            "شیوه ارجاع به پانویس",
            "reference_style",
            [
                "پیش‌فرض",
                "همراه با خط تیره",
            ],
        )

        # دکمه ذخیره
        def save_settings():
            settings["display_mode"] = controls["display_mode"].get()
            settings["separator_position"] = controls[
                "separator_position"
            ].get()
            settings["reference_style"] = controls[
                "reference_style"
            ].get()

            # اعمال نحوه نمایش پانویس در Word
            self._apply_footnote_display_mode()
            
            self._apply_footnote_separator_position()
            
            self._apply_footnote_reference_style()

            close_window()

        save_button = ctk.CTkButton(
            panel,
            text="ذخیره تنظیمات",
            height=40,
            corner_radius=10,
            fg_color=self.blue,
            hover_color=self.blue_hover,
            text_color=self.text,
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=12,
                weight="bold",
            ),
            command=save_settings,
        )
        save_button.pack(fill="x", padx=22, pady=(20, 16))
