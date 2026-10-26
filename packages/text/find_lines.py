DOC = """The lines of a text file that hold a word, with their numbers.

Case is ignored; at most 200 lines are answered."""
CONFIG = {}

import os


def find_lines(path, word, context=None):
    """The lines of the file at path that hold word, case ignored, each as "number: line"."""
    found = []
    with open(os.path.join(context["cwd"], path), encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            if word.lower() in line.lower():
                found.append("%d: %s" % (n, line.rstrip("\n")))
                if len(found) == 200:
                    break
    return found
