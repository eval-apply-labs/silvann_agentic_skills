DOC = """Words, lines and characters counted in a text file.

Read as UTF-8; a word is what lies between spaces, tabs and line ends."""
CONFIG = {}

import os


def count_words(path, context=None):
    """The words, lines and characters of the text file at path."""
    with open(os.path.join(context["cwd"], path), encoding="utf-8", errors="replace") as f:
        text = f.read()
    return {"words": len(text.split()), "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
            "characters": len(text)}
