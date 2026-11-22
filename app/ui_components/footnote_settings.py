"""رابط کاربری پنجره تنظیمات پانویس."""


import customtkinter as ctk


def _add_option_row(app, panel, controls, settings, title, key, options):
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
        fg_color=app.panel_light,
        button_color=app.panel_light,
        button_hover_color=app.blue,
        dropdown_fg_color=app.panel,
        dropdown_hover_color=app.panel_light,
        text_color=app.text,
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
        text_color=app.text,
    )
    label.pack(side="right", padx=8)

    controls[key] = option_menu


def show_footnote_settings_modal(app):
    """نمایش پنجره تنظیمات درج پانویس."""

    # جلوگیری از باز شدن چند پنجره هم‌زمان
    if (
        hasattr(app, "footnote_settings_window")
        and app.footnote_settings_window
        and app.footnote_settings_window.winfo_exists()
    ):
        app.footnote_settings_window.focus()
        return

    # تنظیمات پیش‌فرض
    if not hasattr(app, "footnote_settings"):
        app.footnote_settings = {}

    defaults = {
        "auto_keyboard": True,
        "auto_direction": True,
        "default_language": "فارسی",
        "display_mode": "معمولی",
        "separator_position": "چپ",
        "reference_style": "پیش‌فرض",
    }

    for key, value in defaults.items():
        app.footnote_settings.setdefault(key, value)

    settings = app.footnote_settings

    # ساخت پنجره
    window = ctk.CTkToplevel(app)
    app.footnote_settings_window = window

    window.title("تنظیمات پانویس")
    window.geometry("440x620")
    window.resizable(False, False)
    window.configure(fg_color=app.bg)
    window.transient(app)
    window.grab_set()

    window.update_idletasks()

    x = app.winfo_rootx() + (app.winfo_width() - 440) // 2
    y = app.winfo_rooty() + (app.winfo_height() - 620) // 2

    window.geometry(f"440x620+{x}+{y}")

    def close_window():
        window.destroy()
        app.footnote_settings_window = None

    window.protocol("WM_DELETE_WINDOW", close_window)

    # پنل اصلی
    panel = ctk.CTkFrame(
        window,
        fg_color=app.panel,
        corner_radius=16,
        border_width=1,
        border_color=app.line,
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
        hover_color=app.line,
        text_color=app.muted,
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
        text_color=app.text,
    )
    title.pack(side="right")

    # خط جداکننده
    ctk.CTkFrame(
        panel,
        height=2,
        fg_color=app.blue,
    ).pack(fill="x", padx=18, pady=(0, 14))

    # نگهداری کنترل‌های تنظیمات
    controls = {}

    # نحوه نمایش پانویس
    _add_option_row(
        app,
        panel,
        controls,
        settings,
        "نحوه نمایش پانویس",
        "display_mode",
        [
            "معمولی",
            "دو ستونه",
        ],
    )

    # وضعیت خط جداکننده
    _add_option_row(
        app,
        panel,
        controls,
        settings,
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
    _add_option_row(
        app,
        panel,
        controls,
        settings,
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
        settings["separator_position"] = controls["separator_position"].get()
        settings["reference_style"] = controls["reference_style"].get()

        # اعمال نحوه نمایش پانویس در Word
        app._apply_footnote_display_mode()
        app._apply_footnote_separator_position()
        app._apply_footnote_reference_style()

        close_window()

    save_button = ctk.CTkButton(
        panel,
        text="ذخیره تنظیمات",
        height=40,
        corner_radius=10,
        fg_color=app.blue,
        hover_color=app.blue_hover,
        text_color=app.text,
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=12,
            weight="bold",
        ),
        command=save_settings,
    )
    save_button.pack(fill="x", padx=22, pady=(20, 16))