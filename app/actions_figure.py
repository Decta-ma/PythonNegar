"""اکشن درج عنوان شکل در Word."""

import re


class FigureActions:

    def insert_figure_caption(self):
        try:
            doc = self.engine.ensure_ready()
            word = self.engine.word
            selection = word.Selection

            # استخراج شماره شکل‌های موجود در سند
            text = doc.Content.Text
            numbers = re.findall(r"شکل\s+(\d+)", text)

            next_number = max(map(int, numbers), default=0) + 1
            caption = f"شکل {next_number}"

            # درج در محل فعلی کرسر
            start = selection.Range.Start
            selection.Range.Text = caption

            # انتخاب محل بعد از عنوان درج شده
            end = start + len(caption)
            selection.SetRange(end, end)

            # آوردن Word به جلو و فوکوس روی محل درج
            word.Visible = True
            word.Activate()
            selection.Select()

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "خطا در درج عنوان شکل",
                str(e),
                parent=self
            )