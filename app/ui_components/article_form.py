"""صفحهٔ ورود اطلاعات مقاله و نویسنده‌ها (داخل همان پنجرهٔ اصلی، با انیمیشن موج)."""

import math
import tkinter as tk

import customtkinter as ctk

from .. import theme
from .keyboard_layout import switch_layout

# ---------------------------------------------------------------- رنگ‌ها
# رنگ‌ها از نمونهٔ فرم قبلی (نسخهٔ C#) برداشته شده: صفحهٔ سفید با آبی آسمانی
ACCENT = "#06AEF4"        # آبی اصلی: نوار بالا، دکمهٔ اصلی
ACCENT_DARK = "#007AC1"   # آبی تیره: حلقهٔ موج، حاشیه‌ها
ACCENT_HOVER = "#0597D4"
ACCENT_SOFT = "#B4E7FC"   # آبی خیلی روشن: خط‌جداکننده و حلقهٔ داخلی موج
PAGE_BG = "#FFFFFF"
CARD_BG = "#F2FAFE"
ENTRY_BG = "#FFFFFF"
ENTRY_BORDER = "#434343"
ERROR = "#E53935"
ERROR_TEXT = "#D32F2F"
TEXT = "#1F2937"
MUTED = "#5B6B7A"
ON_ACCENT = "#FFFFFF"     # رنگ نوشته روی آبی
RING = ACCENT_DARK

MIN_NAME_LEN = 5

# (پیشوند کلید فرم، برچسب فارسی، برچسب انگلیسی). کلیدها با build_author و
# build_affiliation یکی‌اند؛ مثلاً "degree" دو کلید degree_fa و degree_en می‌سازد.
_UNIVERSITY_TYPES = {"آزاد": "azad", "دولتی": "dolati"}
_AUTHOR_ROWS = [
    ("name", "نام", "Name"),
    ("degree", "مرتبه علمی", "Degree"),
    ("group", "گروه", "Group"),
    ("faculty", "دانشکده", "Faculty"),
    ("university", "دانشگاه", "University"),
    ("city", "شهر", "City"),
]


def _font(size=13, bold=False):
    return ctk.CTkFont(
        family=theme.FONT_FAMILY, size=size, weight="bold" if bold else "normal"
    )


# ---------------------------------------------------------------- فیلدها
def _make_entry(parent, lang):
    """ورودی متن: فارسی راست‌چین، انگلیسی چپ‌چین، و با ورود به آن کیبورد عوض می‌شود."""
    entry = ctk.CTkEntry(
        parent,
        height=34,
        justify="right" if lang == "fa" else "left",
        fg_color=ENTRY_BG,
        border_color=ENTRY_BORDER,
        text_color=TEXT,
    )
    entry.bind("<FocusIn>", lambda _event, lng=lang: switch_layout(lng), add="+")
    return entry


def _field(parent, label, lang):
    """برچسب بالای ورودی؛ فارسی کاملاً راست، انگلیسی کاملاً چپ. (کادر، ورودی) برمی‌گرداند."""
    box = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(
        box,
        text=label,
        font=_font(12),
        text_color=MUTED,
        anchor="e" if lang == "fa" else "w",
    ).pack(fill="x", pady=(0, 2))
    entry = _make_entry(box, lang)
    entry.pack(fill="x")
    return box, entry


class AuthorBlock(ctk.CTkFrame):
    """کادر اطلاعات یک نویسنده: ستون انگلیسی (چپ) و ستون فارسی (راست)."""

    def __init__(self, master, on_remove):
        super().__init__(
            master,
            fg_color=CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color=ACCENT_SOFT,
        )
        self.entries = {}
        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=1, uniform="col")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=(10, 4))
        self.title_label = ctk.CTkLabel(
            header, text="", font=_font(14, True), text_color=TEXT
        )
        self.title_label.pack(side="right")
        ctk.CTkButton(
            header,
            text="حذف",
            width=60,
            height=28,
            font=_font(12),
            fg_color=ERROR,
            hover_color="#C62828",
            text_color=ON_ACCENT,
            command=lambda: on_remove(self),
        ).pack(side="left")

        for row, (key, label_fa, label_en) in enumerate(_AUTHOR_ROWS, start=1):
            box_en, entry_en = _field(self, label_en, "en")
            box_en.grid(row=row, column=0, sticky="ew", padx=(12, 6), pady=4)
            box_fa, entry_fa = _field(self, label_fa, "fa")
            box_fa.grid(row=row, column=1, sticky="ew", padx=(6, 12), pady=4)
            self.entries[f"{key}_en"] = entry_en
            self.entries[f"{key}_fa"] = entry_fa

        box_email, entry_email = _field(self, "Email", "en")
        box_email.grid(
            row=len(_AUTHOR_ROWS) + 1, column=0, sticky="ew", padx=(12, 6), pady=4
        )
        self.entries["email"] = entry_email

        box_orcid, entry_orcid = _field(self, "ORCID", "en")
        box_orcid.grid(
            row=len(_AUTHOR_ROWS) + 1, column=1, sticky="ew", padx=(6, 12), pady=4
        )
        self.entries["orcid"] = entry_orcid

        options = ctk.CTkFrame(self, fg_color="transparent")
        options.grid(
            row=len(_AUTHOR_ROWS) + 2, column=0, columnspan=2,
            sticky="ew", padx=12, pady=(4, 12),
        )
        self.university_type = ctk.CTkSegmentedButton(
            options, values=list(_UNIVERSITY_TYPES), font=_font(12)
        )
        self.university_type.pack(side="right")
        self.is_responsible = ctk.CTkCheckBox(
            options, text="نویسندهٔ مسئول", font=_font(12), text_color=TEXT
        )
        self.is_responsible.pack(side="left")

    def set_number(self, number):
        self.title_label.configure(text=f"نویسنده {number}")

    def get(self):
        """دیکشنری خام این نویسنده؛ همان ورودی build_author."""
        data = {key: entry.get() for key, entry in self.entries.items()}
        data["university_type"] = _UNIVERSITY_TYPES.get(self.university_type.get(), "")
        data["is_responsible"] = bool(self.is_responsible.get())
        return data


class ArticlePage(ctk.CTkFrame):
    """صفحهٔ فرم مقاله. با تأیید، on_submit(form) صدا زده می‌شود."""

    def __init__(self, master, app, journal, on_submit):
        super().__init__(master, fg_color=PAGE_BG, corner_radius=0)
        self.app = app
        self.journal = journal
        self.on_submit = on_submit
        self.blocks = []

        top = ctk.CTkFrame(self, fg_color=ACCENT, corner_radius=0, height=58)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkLabel(
            top,
            text=f"اطلاعات مقاله | {journal['name']}",
            font=_font(17, True),
            text_color=ON_ACCENT,
        ).pack(side="right", padx=18)
        ctk.CTkButton(
            top,
            text="بازگشت",
            width=80,
            height=30,
            font=_font(12),
            fg_color="transparent",
            border_width=1,
            border_color=ON_ACCENT,
            hover_color=ACCENT_DARK,
            text_color=ON_ACCENT,
            command=self.go_back,
        ).pack(side="left", padx=18)

        box_fa, self.title_fa = _field(self, "عنوان فارسی مقاله", "fa")
        box_fa.pack(fill="x", padx=18, pady=(14, 0))
        box_en, self.title_en = _field(self, "Article title (English)", "en")
        box_en.pack(fill="x", padx=18, pady=(8, 0))

        # نوار پایین اول pack می‌شود تا هیچ‌وقت زیر لبهٔ پنجره نرود
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=18, pady=10)
        ctk.CTkButton(
            bottom,
            text="ساخت مقاله",
            font=_font(14, True),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=ON_ACCENT,
            command=self.submit,
        ).pack(side="right")
        ctk.CTkButton(
            bottom,
            text="افزودن نویسنده",
            font=_font(13),
            fg_color=ACCENT_SOFT,
            hover_color="#9ADBF8",
            text_color=ACCENT_DARK,
            command=self.add_author,
        ).pack(side="left")
        self.error_label = ctk.CTkLabel(
            bottom, text="", font=_font(12), text_color=ERROR_TEXT, anchor="e"
        )
        self.error_label.pack(side="right", fill="x", expand=True, padx=12)

        # فهرست نویسنده‌ها هرچه جای باقی‌مانده است را می‌گیرد و خودش اسکرول می‌خورد
        self.authors_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=120)
        self.authors_frame.pack(fill="both", expand=True, padx=12, pady=(10, 0))

        self.add_author()

    # ------------------------------------------------------------- ناوبری
    def go_back(self):
        from .journal_selection import show_journal_selection

        show_journal_selection(self.app)

    # ------------------------------------------------------------- نویسنده‌ها
    def add_author(self):
        block = AuthorBlock(self.authors_frame, on_remove=self.remove_author)
        block.pack(fill="x", pady=6, padx=4)
        self.blocks.append(block)
        self._renumber()

    def remove_author(self, block):
        if len(self.blocks) == 1:
            self.error_label.configure(text="حداقل یک نویسنده لازم است.")
            return
        self.blocks.remove(block)
        block.destroy()
        self._renumber()

    def _renumber(self):
        for number, block in enumerate(self.blocks, start=1):
            block.set_number(number)

    # ------------------------------------------------------------- ارسال
    def collect(self):
        """کل فرم را به یک دیکشنری خام تبدیل می‌کند (ورودی build_article_info)."""
        return {
            "journal_id": str(self.journal["id"]),
            "title_fa": self.title_fa.get(),
            "title_en": self.title_en.get(),
            "authors": [block.get() for block in self.blocks],
        }

    def _all_entries(self):
        yield self.title_fa
        yield self.title_en
        for block in self.blocks:
            yield from block.entries.values()

    def submit(self):
        for entry in self._all_entries():
            entry.configure(border_color=ENTRY_BORDER)

        problems = []
        if not self.title_fa.get().strip():
            self.title_fa.configure(border_color=ERROR)
            problems.append("عنوان فارسی مقاله را وارد کنید.")

        if not self.blocks:
            problems.append("حداقل یک نویسنده لازم است.")

        for number, block in enumerate(self.blocks, start=1):
            for key, lang_name in (("name_fa", "فارسی"), ("name_en", "انگلیسی")):
                entry = block.entries[key]
                if len(entry.get().strip()) < MIN_NAME_LEN:
                    entry.configure(border_color=ERROR)
                    problems.append(
                        f"نویسنده {number}: نام {lang_name} باید حداقل "
                        f"{MIN_NAME_LEN} کاراکتر باشد."
                    )

        if problems:
            extra = f"  (+{len(problems) - 1} مورد دیگر)" if len(problems) > 1 else ""
            self.error_label.configure(text=problems[0] + extra)
            return

        self.error_label.configure(text="")
        self.on_submit(self.collect())


# ---------------------------------------------------------------- انیمیشن موج
def _snapshot(widget):
    """عکس لحظه‌ای از ناحیهٔ ویجت (تا موج روی صفحهٔ قبلی دیده شود). در صورت خطا None."""
    try:
        from PIL import ImageGrab, ImageTk

        x, y = widget.winfo_rootx(), widget.winfo_rooty()
        w, h = widget.winfo_width(), widget.winfo_height()
        return ImageTk.PhotoImage(ImageGrab.grab(bbox=(x, y, x + w, y + h)))
    except Exception:
        return None


def show_article_form(app, journal, on_submit):
    """از نقطهٔ کلیک، دایره‌ای موجی گسترش می‌یابد و صفحهٔ فرم جای محتوا می‌نشیند."""
    content = app.content
    content.update_idletasks()
    width, height = content.winfo_width(), content.winfo_height()

    # نقطهٔ کلیک = جای ماوس نسبت به ناحیهٔ محتوا
    cx = min(max(app.winfo_pointerx() - content.winfo_rootx(), 0), width)
    cy = min(max(app.winfo_pointery() - content.winfo_rooty(), 0), height)

    photo = _snapshot(content)
    canvas = tk.Canvas(content, highlightthickness=0, bd=0, bg=theme.BG)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    if photo is not None:
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo  # نگه داشتن مرجع، وگرنه عکس پاک می‌شود

    circle = canvas.create_oval(cx, cy, cx, cy, fill=PAGE_BG, outline="")
    ring = canvas.create_oval(cx, cy, cx, cy, outline=RING, width=3)
    ring2 = canvas.create_oval(cx, cy, cx, cy, outline=ACCENT_SOFT, width=2)

    max_radius = math.hypot(max(cx, width - cx), max(cy, height - cy)) + 20
    steps, delay = 30, 15

    def finish():
        # اول صفحهٔ قبلی پاک می‌شود، بعد صفحهٔ جدید (هم‌رنگ دایره) ساخته می‌شود،
        # و آخر بوم حذف می‌شود تا هیچ پرشی دیده نشود
        for child in content.winfo_children():
            if child is not canvas:
                child.destroy()
        page = ArticlePage(content, app, journal, on_submit)
        page.pack(fill="both", expand=True)
        canvas.destroy()

    def step(i):
        t = i / steps
        radius = max_radius * (1 - (1 - t) ** 3)  # شروع سریع، پایان نرم
        canvas.coords(circle, cx - radius, cy - radius, cx + radius, cy + radius)
        outer = radius + 14
        canvas.coords(ring, cx - outer, cy - outer, cx + outer, cy + outer)
        inner = max(radius - 16, 0)
        canvas.coords(ring2, cx - inner, cy - inner, cx + inner, cy + inner)
        if i < steps:
            canvas.after(delay, step, i + 1)
        else:
            finish()

    step(1)