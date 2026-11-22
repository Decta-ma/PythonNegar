"""اکشن درج عنوان جدول در Word."""

import re


class TableActions:
    def insert_table_number(self):
        try:
            doc = self.engine.ensure_ready()
            word = self.engine.word
            selection = word.Selection

            text = doc.Content.Text
            numbers = re.findall(r"جدول\s+(\d+)", text)
            next_number = max(map(int, numbers), default=0) + 1

            caption = f"جدول {next_number}"

            start = selection.Range.Start
            selection.Range.Text = caption
            end = start + len(caption)

            # اعمال فونت روی Range دقیق متن
            caption_range = doc.Range(start, end)
            caption_range.Font.Name = "B Zar"
            caption_range.Font.NameBi = "B Zar"
            caption_range.Font.Italic = True
            caption_range.Font.ItalicBi = True

            # انتقال کرسر به بعد از متن
            selection.SetRange(end, end)

            word.Visible = True
            word.Activate()
            selection.Select()

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("خطا در درج شماره جدول", str(e), parent=self)