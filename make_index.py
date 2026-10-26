#!/usr/bin/env python3
"""index.json written from packages/ — what SiLVANN's (list_repo) and (list_package …) read, and the SHA-256 its
(get_tool …) checks a tool's file against. Each tool is read as SiLVANN's (add_tool …) reads it — its DOC, its CONFIG,
each function whose name does not start with _ a command — with Python's ast, never run.

  python3 make_index.py            write index.json
  python3 make_index.py --check    exit 1 where index.json is not what packages/ say
"""
import ast
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "silvann agentic skills repository"
DESCRIPTION = "tools for SiLVANN's REPL, a package a folder, each tool one Python file its (add_tool …) installs"
TOOL_NAME = re.compile(r"[a-z][a-z0-9_-]{0,39}")


def tool(path):
    source = open(path, encoding="utf-8").read()
    tree = ast.parse(source)
    fields = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("DOC", "CONFIG"):
                    fields[t.id] = ast.literal_eval(node.value)
    doc = fields.get("DOC", ast.get_docstring(tree) or "")
    verbs = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            names = [a.arg for a in node.args.args if a.arg != "context"]
            optional = len(node.args.defaults) - (1 if any(a.arg == "context" for a in node.args.args) else 0)
            usage = " ".join(n if i < len(names) - max(optional, 0) else "[%s]" % n for i, n in enumerate(names))
            name = node.name.replace("_", "-")
            verbs.append({"name": name, "usage": "(%s%s)" % (name, " " + usage if usage else ""),
                          "about": (ast.get_docstring(node) or "").strip().split("\n")[0]})
    if not verbs:
        raise SystemExit("%s has no command: a function whose name does not start with _ is one" % path)
    return {"file": os.path.relpath(path, HERE).replace(os.sep, "/"),
            "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "doc": doc.strip().split("\n")[0], "verbs": verbs, "settings": sorted(fields.get("CONFIG", {}))}


def index():
    packages = {}
    root = os.path.join(HERE, "packages")
    for name in sorted(os.listdir(root)):
        folder = os.path.join(root, name)
        if not os.path.isdir(folder):
            continue
        text = open(os.path.join(folder, "PACKAGE.md"), encoding="utf-8").read().strip()
        first, _, rest = text.partition("\n")
        tools = {}
        for f in sorted(os.listdir(folder)):
            if f.endswith(".py"):
                if not TOOL_NAME.fullmatch(f[:-3]):
                    raise SystemExit("%s/%s: a tool's name is lowercase letters, digits, - and _" % (name, f))
                tools[f[:-3]] = tool(os.path.join(folder, f))
        packages[name] = {"description": first.strip(), "about": rest.strip(), "tools": tools}
    return {"name": NAME, "description": DESCRIPTION, "packages": packages}


def main():
    text = json.dumps(index(), indent=1, ensure_ascii=False) + "\n"
    path = os.path.join(HERE, "index.json")
    if "--check" in sys.argv:
        same = os.path.isfile(path) and open(path, encoding="utf-8").read() == text
        print("index.json is %s" % ("what packages/ say" if same else "NOT what packages/ say: run make_index.py"))
        sys.exit(0 if same else 1)
    open(path, "w", encoding="utf-8").write(text)
    print("index.json: %d packages, %d tools" % (len(json.loads(text)["packages"]),
                                                 sum(len(p["tools"]) for p in json.loads(text)["packages"].values())))


if __name__ == "__main__":
    main()
