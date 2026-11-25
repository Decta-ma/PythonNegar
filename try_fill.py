from pathlib import Path

from app.word_engine import WordEngine
from app.article.models import ArticleInfo, Author, Affiliation
from app.article.word_fill import fill_document

info = ArticleInfo(
    journal_id="ebtekar",
    title_fa="عنوان آزمایشی مقاله",
    title_en="Test Article Title",
    authors=[
        Author(
            name_fa="علی رضایی", name_en="Ali Rezaei",
            affiliation=Affiliation(
                degree_fa="دانشجوی دکتری", degree_en="PhD Student",
                university_fa="دانشگاه یزد", university_en="Yazd University",
                city_fa="یزد", city_en="Yazd",
            ),
        ),
        Author(name_fa="سارا احمدی", name_en="Sara Ahmadi"),
    ],
)

engine = WordEngine()
template = Path.home() / "Documents" / "PythonNegar" / "Templates" / "Ebtekar.dotx"
engine.create_new_signed_doc(str(Path.home() / "Documents" / "test_fill.docx"), template)
fill_document(engine.doc, info)