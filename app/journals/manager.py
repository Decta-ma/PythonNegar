from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path

_REQUIRED = {
    "id", "name", "page", "fonts", "header", "styles"
}

def _is_journal_config(value):
    return(
        isinstance(value, dict)
        and _REQUIRED.issubset(value)
    )


def get_journals():
    journals = {}
    package_dir = Path(__file__).resolve().parent

    for module_info in iter_modules([str(package_dir)]):

        if module_info.name in {
            "manager",
            "template_builder"
        }:
            continue

        if module_info.name.startswith("_"):
            continue

        module = import_module(
            f"{__package__}.{module_info.name}"
        )

        preferred = getattr(module, "JOURNAL", None)

        candidates = (
            [preferred]
            if _is_journal_config(preferred)
            else []
        )

        if not candidates:
            candidates = [
                value
                for name, value in vars(module).items()
                if name.isupper()
                and _is_journal_config(value)
            ]

            for config in candidates:
                journals[str(config["id"])] = config

        return sorted(
            journals.values(),
            key=lambda item : item["name"].casefold() 
        )

    def get_journal(journal_id):

        for journal in get_journals():
            if str(journal["id"]) == str(journal_id):
                return journal

        raise KeyError(f"ژرنالی پیدا نشد: {journal_id}")


