DOC = """A CSV file's columns: their names, or one column's values.

The file's first line names its columns."""
CONFIG = {}

import csv
import os


def _rows(path, context):
    with open(os.path.join(context["cwd"], path), newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def csv_names(path, context=None):
    """The names of the CSV file's columns, in order."""
    with open(os.path.join(context["cwd"], path), newline="", encoding="utf-8", errors="replace") as f:
        return next(csv.reader(f), [])


def csv_column(path, name, context=None):
    """The values of one column of the CSV file, top to bottom."""
    rows = _rows(path, context)
    if rows and name not in rows[0]:
        raise ValueError("no column %r: the columns are %s" % (name, ", ".join(rows[0])))
    return [r[name] for r in rows]
