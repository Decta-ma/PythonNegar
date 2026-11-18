"""منوی کشویی شیشه‌ای (Liquid Glass) با انیمیشن نرم برای CustomTkinter.

ایدهٔ کار:
  * tkinter قابلیت «محو کردن پشت پنجره» ندارد، پس پیش از باز شدن منو از ناحیهٔ
    زیر آن اسکرین‌شات می‌گیریم، محو (Blur) و رنگ‌دارش می‌کنیم و به‌عنوان پس‌زمینه
    می‌گذاریم. نتیجه ظاهر شیشهٔ مات (Frosted Glass) مثل iOS است.
  * انیمیشن‌ها بر پایهٔ «زمان واقعی» و کاهش نمایی هستند، بنابراین روی هر سیستمی
    نرم و بدون پرش اجرا می‌شوند.
"""

import math
import time
import tkinter as tk
from tkinter import font as tkfont

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageGrab, ImageTk

# رنگی که ویندوز آن را کاملاً شفاف می‌کند (برای گوشه‌های گرد پنجره)
KEY_COLOR = "#010203"
KEY_RGB = (1, 2, 3)

# رنگ‌های هماهنگ با پالت برنامه
GLASS_RGB = (28, 44, 92)       # رنگ پایهٔ شیشه
TEXT_RGB = (248, 250, 252)     # متن آیتم‌ها
SUB_RGB = (191, 219, 254)      # متن زیرآیتم‌ها
ACCENT_RGB = (96, 165, 250)    # آیتم بازشده


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(int(max(0, min(255, v))) for v in rgb)


def _mix(c1, c2, t):
    """ترکیب دو رنگ؛ t=0 رنگ اول، t=1 رنگ دوم."""
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))


def _approach(value, target, factor):
    """نزدیک‌شدن نرم (نمایی) مقدار به هدف؛ نزدیک هدف دقیقاً روی آن می‌نشیند."""
    if abs(target - value) < 0.003:
        return target
    return value + (target - value) * factor


class _Node:
    """یک آیتم منو. p پیشرفت فعلی بازشدن و target مقدار مقصد (۰ یا ۱) است."""

    def __init__(self, label, children=None, parent=None):
        self.label = label
        self.parent = parent
        self.children = [_Node(c, None, self) for c in (children or [])]
        self.p = 0.0
        self.target = 0.0


class GlassDropdown:
    ROW_H = 42
    PAD = 8
    RADIUS = 18
    MIN_W = 250

    def __init__(self, master, anchor, items, on_select=None, scale=1.0):
        """
        master   : پنجرهٔ اصلی برنامه
        anchor   : ویجتی (کارت) که منو زیر آن باز می‌شود
        items    : [(عنوان, [زیرآیتم‌ها] یا None), ...]
        on_select: تابعی که مسیر آیتم انتخاب‌شده را می‌گیرد، مثل ("تبدیل اعداد", "به فارسی")
        scale    : ضریب بزرگ‌نمایی صفحه (DPI)
        """
        self.master = master
        self.anchor = anchor
        self.on_select = on_select
        self.S = scale

        self.nodes = [_Node(label, kids) for label, kids in items]
        self.rootp = 0.0
        self.root_target = 1.0
        self.hover = None
        self.rows = []
        self.top = None
        self._after = None
        self._alive = False
        self._closing = False
        self._selected = None
        self._photo = None
        self._last = 0.0

    @property
    def is_open(self):
        return self._alive and not self._closing

    # ------------------------------------------------------------------ باز کردن
    def open(self):
        S = self.S
        self.row_h = int(self.ROW_H * S)
        self.pad = int(self.PAD * S)
        self.radius = int(self.RADIUS * S)

        anchor = self.anchor
        anchor.update_idletasks()
        self.w = max(anchor.winfo_width(), int(self.MIN_W * S))

        # بلندترین حالت ممکن (یک گروه کامل باز) برای گرفتن پس‌زمینه
        max_rows = len(self.nodes) + max((len(n.children) for n in self.nodes), default=0)
        self.max_h = max_rows * self.row_h + 2 * self.pad

        # جای منو: زیر کارت؛ اگر جا نبود، بالای کارت
        gap = int(6 * S)
        screen_w, screen_h = anchor.winfo_screenwidth(), anchor.winfo_screenheight()
        card_top = anchor.winfo_rooty()
        card_bottom = card_top + anchor.winfo_height()
        self.up = card_bottom + gap + self.max_h > screen_h - int(40 * S)
        self.anchor_y = (card_top - gap) if self.up else (card_bottom + gap)
        self.x = max(0, min(anchor.winfo_rootx(), screen_w - self.w - int(8 * S)))

        # اسکرین‌شات باید قبل از ساخت پنجرهٔ منو گرفته شود
        glass_y = self.anchor_y - self.max_h if self.up else self.anchor_y
        self._glass = self._build_glass(self.x, glass_y, self.w, self.max_h)

        top = tk.Toplevel(self.master)
        top.withdraw()
        top.overrideredirect(True)
        top.attributes("-topmost", True)
        top.attributes("-alpha", 0.0)
        try:
            top.attributes("-transparentcolor", KEY_COLOR)
        except tk.TclError:
            pass
        top.configure(bg=KEY_COLOR)
        self.top = top

        self.canvas = tk.Canvas(
            top, width=self.w, height=2, bg=KEY_COLOR,
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self.canvas.pack()
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw")

        self.f_main = tkfont.Font(root=self.master, family="Vazirmatn",
                                  size=-int(15 * S), weight="bold")
        self.f_sub = tkfont.Font(root=self.master, family="Vazirmatn",
                                 size=-int(14 * S))

        top.bind("<Button-1>", self._on_click)
        top.bind("<Escape>", lambda e: self.close())
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Leave>", self._on_leave)

        self._alive = True
        self._render()
        top.deiconify()
        top.after(30, self._grab_input)
        self._schedule()

    def _grab_input(self):
        """تمام کلیک‌ها به منو می‌رسد تا کلیک بیرون از آن را تشخیص دهیم."""
        if not self._alive:
            return
        try:
            self.top.focus_force()
            self.top.grab_set()
        except tk.TclError:
            self.top.after(30, self._grab_input)

    # --------------------------------------------------------------- پس‌زمینهٔ شیشه
    def _build_glass(self, x, y, w, h):
        try:
            shot = ImageGrab.grab(bbox=(x, y, x + w, y + h), all_screens=True).convert("RGB")
            if shot.size != (w, h):
                shot = shot.resize((w, h))
        except Exception:
            shot = Image.new("RGB", (w, h), GLASS_RGB)

        glass = shot.filter(ImageFilter.GaussianBlur(radius=16 * self.S))   # محو
        glass = ImageEnhance.Color(glass).enhance(1.4)                      # رنگ‌های زنده‌تر
        glass = Image.blend(glass, Image.new("RGB", (w, h), GLASS_RGB), 0.55)  # رنگ شیشه

        # درخشش ملایم لبهٔ بالا
        grad = Image.linear_gradient("L").resize((w, h)).point(lambda v: int((255 - v) * 0.16))
        return Image.composite(Image.new("RGB", (w, h), (255, 255, 255)), glass, grad)

    # ----------------------------------------------------------------- چیدمان
    def _layout(self):
        rows = []

        def walk(nodes, scale, y, depth):
            for node in nodes:
                h = self.row_h * scale
                rows.append((node, y, h, depth, scale))
                y += h
                if node.children and node.p > 0.001:
                    y = walk(node.children, scale * node.p, y, depth + 1)
            return y

        y = walk(self.nodes, self.rootp, self.pad * self.rootp, 0)
        return rows, y + self.pad * self.rootp

    # ----------------------------------------------------------------- رسم
    def _render(self):
        if not self._alive:
            return
        S, W = self.S, self.w
        rows, content_h = self._layout()
        self.rows = rows
        H = max(2, min(self.max_h, int(round(content_h))))
        R = min(self.radius, H // 2)

        # --- ۱) پنجره
        wy = self.anchor_y - H if self.up else self.anchor_y
        self.top.geometry(f"{W}x{H}+{self.x}+{wy}")
        self.canvas.configure(height=H)
        self.top.attributes("-alpha", min(1.0, self.rootp * 1.5))

        # --- ۲) تصویر شیشه با گوشه‌های گرد، حاشیه و هایلایت
        SS = 2
        big = (W * SS, H * SS)
        mask = Image.new("L", big, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, big[0] - 1, big[1] - 1), radius=R * SS, fill=255)
        mask = mask.resize((W, H), Image.LANCZOS)

        overlay = Image.new("RGBA", big, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        d.rounded_rectangle((0, 0, big[0] - 1, big[1] - 1), radius=R * SS,
                            outline=(255, 255, 255, 80), width=SS)
        for node, y, h, depth, sc in rows:
            if node is self.hover and sc > 0.6:
                m = int(8 * S)
                d.rounded_rectangle((m * SS, int((y + 2) * SS), (W - m) * SS, int((y + h - 2) * SS)),
                                    radius=int(10 * S) * SS, fill=(255, 255, 255, 40))
        overlay = overlay.resize((W, H), Image.LANCZOS)

        if self.up:
            box = (0, self.max_h - H, W, self.max_h)
        else:
            box = (0, 0, W, H)
        base = self._glass.crop(box).convert("RGBA")
        base.alpha_composite(overlay)
        out = Image.new("RGB", (W, H), KEY_RGB)
        out.paste(base.convert("RGB"), (0, 0), mask)

        self._photo = ImageTk.PhotoImage(out, master=self.top)
        self.canvas.itemconfigure(self.bg_item, image=self._photo)

        # --- ۳) متن‌ها و فلش‌ها
        c = self.canvas
        c.delete("dyn")
        for node, y, h, depth, sc in rows:
            if sc < 0.15:
                continue
            fade = ((sc - 0.15) / 0.85) ** 2        # با کوچک‌شدن ردیف، متن محو می‌شود
            cy = y + h / 2
            if depth == 0:
                rgb = _mix(TEXT_RGB, ACCENT_RGB, node.p)
                font, x = self.f_main, W - 20 * S
            else:
                rgb, font, x = SUB_RGB, self.f_sub, W - 38 * S
            color = _hex(_mix(GLASS_RGB, rgb, fade))
            c.create_text(x, cy, text=node.label, anchor="e", fill=color, font=font, tags="dyn")
            if node.children:
                self._chevron(20 * S + 4 * S, cy, node.p, color)

    def _chevron(self, cx, cy, p, color):
        """فلش که با باز شدن آیتم از «>» به «v» می‌چرخد."""
        S = self.S
        a = math.pi - (math.pi / 2) * p          # زاویهٔ جهت فلش
        size = 5 * S
        tip_x, tip_y = cx + math.cos(a) * size * 0.6, cy + math.sin(a) * size * 0.6
        pts = []
        for sign in (1, -1):
            ang = a + math.pi + sign * math.pi / 4
            pts += [tip_x + math.cos(ang) * size, tip_y + math.sin(ang) * size]
        self.canvas.create_line(pts[0], pts[1], tip_x, tip_y, pts[2], pts[3],
                                fill=color, width=max(1, int(2 * S)),
                                capstyle="round", joinstyle="round", tags="dyn")

    # --------------------------------------------------------------- انیمیشن
    def _schedule(self):
        if self._after is None and self._alive:
            self._last = time.perf_counter()
            self._after = self.top.after(8, self._tick)

    def _tick(self):
        self._after = None
        if not self._alive:
            return
        now = time.perf_counter()
        dt = min(now - self._last, 0.05)
        self._last = now
        f = 1 - math.exp(-16 * dt)

        self.rootp = _approach(self.rootp, self.root_target, f)
        moving = self.rootp != self.root_target
        for node in self.nodes:
            if node.children:
                node.p = _approach(node.p, node.target, f)
                moving = moving or node.p != node.target

        self._render()

        if self._closing and self.rootp <= 0.02:
            self._finish()
            return
        if moving:
            self._after = self.top.after(8, self._tick)

    # ------------------------------------------------------------- رویدادها
    def _hit(self, local_y):
        for node, y, h, depth, sc in self.rows:
            if sc > 0.6 and y <= local_y < y + h:
                return node
        return None

    def _on_motion(self, event):
        node = self._hit(event.y_root - self.top.winfo_rooty())
        if node is not self.hover:
            self.hover = node
            if self._after is None:
                self._render()

    def _on_leave(self, _event):
        if self.hover is not None:
            self.hover = None
            if self._after is None:
                self._render()

    def _on_click(self, event):
        if self._closing or not self._alive:
            return
        lx = event.x_root - self.top.winfo_rootx()
        ly = event.y_root - self.top.winfo_rooty()
        if lx < 0 or ly < 0 or lx >= self.w or ly >= self.top.winfo_height():
            self.close()                          # کلیک بیرون از منو
            return

        node = self._hit(ly)
        if node is None:
            return
        if node.children:                         # آیتم دارای زیرمنو: باز/بسته
            if node.target:
                node.target = 0.0
            else:
                for other in self.nodes:          # هر بار فقط یک گروه باز می‌ماند
                    other.target = 0.0
                node.target = 1.0
            self._schedule()
        else:                                     # آیتم نهایی: انتخاب و بستن
            self._selected = (node.parent.label, node.label) if node.parent else (node.label,)
            self.close()

    # ----------------------------------------------------------------- بستن
    def close(self):
        if not self._alive or self._closing:
            return
        self._closing = True
        self.root_target = 0.0
        self._schedule()

    def _finish(self):
        self._alive = False
        if self._after is not None:
            try:
                self.top.after_cancel(self._after)
            except Exception:
                pass
            self._after = None
        try:
            self.top.grab_release()
        except Exception:
            pass
        self.top.destroy()

        if self.on_select and self._selected:
            path = self._selected
            self.master.after(10, lambda: self.on_select(path))
