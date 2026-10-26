DOC = """A value in a JSON file, at a path of keys and indexes.

The path is its keys and list indexes joined by dots: "orders.0.total"."""
CONFIG = {}

import json
import os


def json_value(path, keys, context=None):
    """The value in the JSON file at path found by keys, dot-joined ("" the whole file)."""
    with open(os.path.join(context["cwd"], path), encoding="utf-8") as f:
        value = json.load(f)
    for key in [k for k in str(keys).split(".") if k != ""]:
        if isinstance(value, list):
            if not key.lstrip("-").isdigit():
                raise ValueError("%r is not a list's index" % key)
            value = value[int(key)]
        elif isinstance(value, dict):
            if key not in value:
                raise ValueError("no key %r: the keys are %s" % (key, ", ".join(map(str, value))))
            value = value[key]
        else:
            raise ValueError("%r: the value before it has no keys" % key)
    return value
