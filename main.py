"""نقطهٔ ورود داخلی پکیج (اجرا از پوشهٔ article_negar_modular)."""

import os
import sys

# اطمینان از در دسترس بودن پوشهٔ والد برای ایمپورت پکیج app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.ui import LuxuryWordAssistant
except ImportError:  # اجرای مستقیم فایل داخل پکیج
    from app.ui import LuxuryWordAssistant


def main():
    app = LuxuryWordAssistant()
    app.mainloop()


if __name__ == "__main__":
    main()
