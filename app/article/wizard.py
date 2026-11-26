from dataclasses import dataclass
from app.article.models import Author

@dataclass
def build_author_list(form):
    return Author(
        name_fa = form.get("name_fa", "").strip(),
        name_En = form.get("name_en", "").strip(),
        email = form.get("email", "").strip()
    )
