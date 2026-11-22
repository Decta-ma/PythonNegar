"""منوی راهنمای برنامه."""

import webbrowser

from ..glass_dropdown import GlassDropdown


HELP_LINKS = {
    "دسترسی به سامانه فصل‌نامه": "https://sanad.iau.ir/journal/ichs",
    "راهنمای نوشتن مقاله": "https://shivanegar.ir/ArticleWritingGuide.pdf",
    "راهنمای نوشتن چکیده مبسوط": "https://shivanegar.ir/ExtendedAbstract.pdf",
}


def show_help_menu(app, anchor):
    """نمایش منوی کشویی راهنما."""

    items = [
        ("دسترسی به سامانه فصل‌نامه", None),
        ("راهنمای نوشتن مقاله", None),
        ("راهنمای نوشتن چکیده مبسوط", None),
    ]

    def handle_selection(path):
        selected_item = path[0]
        url = HELP_LINKS.get(selected_item)

        if url:
            webbrowser.open_new_tab(url)

    # جلوگیری از باز شدن چند منو به‌صورت هم‌زمان
    if hasattr(app, "help_dropdown"):
        current_dropdown = app.help_dropdown

        if current_dropdown and current_dropdown.is_open:
            return

    app.help_dropdown = GlassDropdown(
        master=app,
        anchor=anchor,
        items=items,
        on_select=handle_selection,
    )

    app.help_dropdown.open()