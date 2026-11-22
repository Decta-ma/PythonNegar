from dataclasses import dataclass, field
from enum import Enum 

class UniversityType(Enum):
    AZAD = "azad"
    DOLATI = "dolati"

@dataclass 
class Affiliation:
    university_type: UniversityType = None 
    degree_fa: str = ""
    degree_en: str = ""
    group_fa: str = ""
    group_en: str = ""
    faculty_fa: str = ""
    faculty_en: str = ""
    university_fa: str = ""
    university_en: str = ""
    city_fa: str = ""
    city_en: str = ""


@dataclass
class Author:
    name_fa: str
    name_en: str
    email: str = ""
    orcid: str = ""
    is_responsible: bool = False 
    affiliation: Affiliation = field(default_factory=Affiliation)


@dataclass 
class ArticleInfo:
    journal_id: str
    title_fa: str
    title_en: str
    author: list = field(default_factory=list)
