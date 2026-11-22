"""رابط کاربری پنجره تنظیمات ویراستاری."""

import customtkinter as ctk


def _add_settings_switch(app, parent, text, key, default=False):
    """ساخت یک گزینه روشن/خاموش در تنظیمات ویراستاری."""

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
        text_color=app.text,
        anchor="e",
    )
    label.pack(side="right", fill="both", expand=True, padx=8)

    switch = ctk.CTkSwitch(
        row,
        text="",
        width=42,
        progress_color=app.blue,
        button_color="#F8FAFC",
        button_hover_color="#CBD5E1",
        fg_color=app.line,
        onvalue=True,
        offvalue=False,
    )
    switch.pack(side="left", padx=8)

    if default:
        switch.select()
    else:
        switch.deselect()

    app.editing_settings_controls[key] = switch

    return switch


def show_editing_settings_modal(app):
    """نمایش پنجره تنظیمات ویراستاری."""

    # جلوگیری از باز شدن چند پنجره هم‌زمان
    if (
        hasattr(app, "editing_settings_window")
        and app.editing_settings_window
        and app.editing_settings_window.winfo_exists()
    ):
        app.editing_settings_window.lift()
        return

    modal = ctk.CTkToplevel(app)
    app.editing_settings_window = modal

    modal.title("تنظیمات ویراستاری")
    modal.geometry("460x590")
    modal.resizable(False, False)
    modal.configure(fg_color=app.bg)

    modal.transient(app)
    modal.grab_set()

    # قرار گرفتن پنجره در مرکز برنامه
    app.update_idletasks()

    x = app.winfo_rootx() + (app.winfo_width() - 460) // 2
    y = app.winfo_rooty() + (app.winfo_height() - 590) // 2

    modal.geometry(f"460x590+{x}+{y}")

    # نگهداری کنترل‌های تنظیمات
    app.editing_settings_controls = {}

    # قاب اصلی
    main = ctk.CTkFrame(
        modal,
        fg_color=app.panel,
        corner_radius=16,
        border_width=1,
        border_color=app.line,
    )
    main.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10,
    )

    # سربرگ
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
        hover_color=app.panel_light,
        text_color=app.muted,
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
        text_color=app.text,
    ).pack(side="right")

    # خط جداکننده
    ctk.CTkFrame(
        main,
        height=2,
        fg_color=app.blue,
    ).pack(fill="x", padx=16, pady=(0, 12))

    # بخش ویراستار
    ctk.CTkLabel(
        main,
        text="ویراستار",
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=12,
            weight="bold",
        ),
        text_color=app.blue_hover,
    ).pack(anchor="e", padx=20, pady=(4, 8))

    _add_settings_switch(
        app,
        main,
        "اصلاح نیم‌فاصله در پانویس‌ها",
        "footnotes",
    )

    _add_settings_switch(
        app,
        main,
        "اصلاح نیم‌فاصله در سرصفحه و پاصفحه",
        "headers_footers",
    )

    _add_settings_switch(
        app,
        main,
        "اصلاح نیم‌فاصله در فیلدهای خاص",
        "special_fields",
    )

    _add_settings_switch(
        app,
        main,
        "ویرایش‌های نشانه‌گذاری‌شده به کاربر نمایش داده شود",
        "show_revisions",
        default=True,
    )

    # بخش تبدیل اعداد
    ctk.CTkFrame(
        main,
        height=2,
        fg_color=app.line,
    ).pack(fill="x", padx=16, pady=(14, 10))

    ctk.CTkLabel(
        main,
        text="تبدیل اعداد",
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=12,
            weight="bold",
        ),
        text_color=app.blue_hover,
    ).pack(anchor="e", padx=20, pady=(2, 8))

    _add_settings_switch(
        app,
        main,
        "جایگزین کردن کاراکتر عدد",
        "replace_number_character",
    )

    # بخش شعر
    ctk.CTkFrame(
        main,
        height=2,
        fg_color=app.line,
    ).pack(fill="x", padx=16, pady=(14, 10))

    ctk.CTkLabel(
        main,
        text="شعر",
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=12,
            weight="bold",
        ),
        text_color=app.blue_hover,
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
        text_color=app.muted,
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
        fg_color=app.panel_light,
        button_color=app.blue,
        button_hover_color=app.blue_hover,
        text_color=app.text,
        dropdown_fg_color=app.panel,
        dropdown_hover_color=app.panel_light,
        dropdown_text_color=app.text,
        dynamic_resizing=False,
    )

    poetry_menu.set("به صورت ستونی")
    poetry_menu.pack(fill="x")

    app.editing_settings_controls["poetry_style"] = poetry_menu