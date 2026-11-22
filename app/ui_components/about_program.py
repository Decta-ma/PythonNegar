"""رابط کاربری منوی درباره برنامه و پنجره اطلاعات مقاله‌نگار."""

import webbrowser
import customtkinter as ctk

from ..glass_dropdown import GlassDropdown


GUIDE_VIDEOS_URL = "https://shivanegar.ir/videos/4"
SHIVANEGAR_URL = "https://shivanegar.ir/"

def show_about_program_menu(app, anchor):
    """نمایش منوی کشویی کارت درباره برنامه."""

    items = [
        ("آرشیو فیلم های راهنما", None),
        ("سامانه شیوانگار", None),
        ("درباره مقاله نگار", None),
    ]

    def handle_selection(path):
        """مدیریت انتخاب آیتم منو."""

        selected_item = path[0]

        if selected_item == "آرشیو فیلم های راهنما":
            webbrowser.open_new_tab(GUIDE_VIDEOS_URL)

        elif selected_item == "سامانه شیوانگار":
            webbrowser.open_new_tab(SHIVANEGAR_URL)

        elif selected_item == "درباره مقاله نگار":
            show_about_program_modal(app)

    # جلوگیری از باز شدن چند منو به‌صورت هم‌زمان
    if hasattr(app, "about_program_dropdown"):
        current_dropdown = app.about_program_dropdown

        if current_dropdown and current_dropdown.is_open:
            return

    app.about_program_dropdown = GlassDropdown(
        master=app,
        anchor=anchor,
        items=items,
        on_select=handle_selection,
    )

    app.about_program_dropdown.open()


def show_about_program_modal(app):
    """نمایش پنجره اطلاعات و حقوق نرم‌افزار مقاله‌نگار."""

    # جلوگیری از باز شدن چند پنجره هم‌زمان
    if (
        hasattr(app, "about_program_window")
        and app.about_program_window
        and app.about_program_window.winfo_exists()
    ):
        app.about_program_window.lift()
        return

    window = ctk.CTkToplevel(app)
    app.about_program_window = window

    window.title("درباره مقاله نگار")
    window.geometry("460x380")
    window.resizable(False, False)
    window.configure(fg_color="#F4F0F8")
    window.transient(app)
    window.grab_set()

    # قرار دادن پنجره در مرکز برنامه
    window.update_idletasks()

    x = app.winfo_rootx() + (app.winfo_width() - 460) // 2
    y = app.winfo_rooty() + (app.winfo_height() - 380) // 2

    window.geometry(f"460x380+{x}+{y}")

    def close_window():
        window.destroy()
        app.about_program_window = None

    window.protocol("WM_DELETE_WINDOW", close_window)

    # سربرگ پنجره
    header = ctk.CTkFrame(
        window,
        fg_color="#F4F0F8",
        corner_radius=0,
        height=42,
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="درباره مقاله نگار",
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=12,
        ),
        text_color="#111827",
    ).pack(side="right", padx=12)

    ctk.CTkButton(
        header,
        text="×",
        width=32,
        height=32,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#E5DFEB",
        text_color="#111827",
        font=ctk.CTkFont(size=20),
        command=close_window,
    ).pack(side="left", padx=8)

    # کارت سفید اطلاعات
    info_card = ctk.CTkFrame(
        window,
        fg_color="#FFFFFF",
        corner_radius=8,
        border_width=1,
        border_color="#E5E7EB",
    )
    info_card.pack(
        fill="both",
        expand=True,
        padx=26,
        pady=(34, 48),
    )

    # عنوان برنامه
    ctk.CTkLabel(
        info_card,
        text="مقاله نگار",
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=22,
            weight="bold",
        ),
        text_color="#111111",
    ).pack(anchor="e", padx=24, pady=(26, 12))

    # اطلاعات نسخه و کپی‌رایت
    details = [
        "نسخه: ۱.۳.۲",
        "کپی‌رایت: © ۲۰۲۰-۲۰۲۵",
        "شرکت: ویرا پژوهان بهین فراتاک",
    ]

    for detail in details:
        ctk.CTkLabel(
            info_card,
            text=detail,
            font=ctk.CTkFont(
                family="Vazirmatn",
                size=10,
            ),
            text_color="#555555",
        ).pack(anchor="e", padx=24, pady=5)

    # متن حقوق نرم‌افزار
    copyright_text = (
        "تمامی حقوق مادی و معنوی این نرم‌افزار (افزونه)،\n"
        "متعلق به شرکت ویرا پژوهان بهین فراتاک است؛\n"
        "لذا هرگونه نسخه‌برداری از برنامه یا بخش‌هایی از آن پیگرد قانونی دارد."
    )

    ctk.CTkLabel(
        info_card,
        text=copyright_text,
        font=ctk.CTkFont(
            family="Vazirmatn",
            size=10,
        ),
        text_color="#555555",
        justify="right",
        anchor="e",
    ).pack(
        anchor="e",
        padx=24,
        pady=(8, 18),
    )