"""اکشن درج معادله در Word."""

class EquationActions:

    def equation_action(self):
        try:
            doc = self.engine.ensure_ready()
            word = self.engine.word
            selection = word.Selection

            doc.OMaths.Add(selection.Range)

            equation = doc.OMaths(doc.OMaths.Count)
            equation.BuildUp()

            word.Visible = True
            word.Activate()
            equation.Range.Select()

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "خطا در درج معادله",
                str(e),
                parent=self
            )