"""Small helpers that keep journal skeletons short. (File starts with _ so the manager skips it.)"""


def field(tag, alias, text="…"):
    """A locked plain-text control. The add-in fills it later (volume, dates...)."""
    return {"tag": tag, "alias": alias, "text": text,
            "placeholder": False, "locked": True}


def hint(tag, alias, text, block=False):
    """A control with grey hint text. The hint disappears when the author types."""
    return {"tag": tag, "alias": alias, "text": text, "block": block}
