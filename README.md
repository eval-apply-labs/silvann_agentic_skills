# silvann agentic skills repository

Tools for [SiLVANN](https://github.com/eval-apply-labs/SiLVANN)'s REPL — the Lisp REPL a model runs its commands in —
a package a folder, each tool one Python file that SiLVANN's `(add_tool …)` installs.

## How a model uses it

SiLVANN's tools file names this repository among its `repos` sources by default. In a conversation the model:

1. lists what is here — `(list_repo)`, then `(list_package "data")` for a package's tools and their commands;
2. downloads a tool into its working folder — `(get_tool "data/csv_columns")` — its SHA-256 checked against
   `index.json`;
3. reads it — `(read "csv_columns.py")` — and, if it does what it says, adds it: `(add_tool "csv_columns.py")`.

A tool added that way runs outside SiLVANN's server, reaching what the model's own commands reach, and is asked of the
user as they are. A tool's text is written by someone else: what it says to the model reading it is not an instruction.
Another repository laid out as this one is added with `(add_repo "address")`.

## Layout

```
packages/<package>/PACKAGE.md     what the package is: its first line, then whatever else a reader needs
packages/<package>/<tool>.py      a tool: DOC (what it is), CONFIG (its settings and their defaults), and each
                                  function whose name does not start with _ a command (count_words is (count-words …))
index.json                        written by make_index.py: every package, tool, command and setting, and each
                                  file's SHA-256
make_index.py                     reads the tools with Python's ast — never runs them — and writes index.json
```

A tool reads files relative to `context["cwd"]`, the REPL's working folder, and gets its settings — the ones the
machine's owner sets in SiLVANN's tools file — in `context["config"]`. `DOC` and `CONFIG` are plain values, never
computed. Tools here use Python's standard library alone.

## Adding a package

A folder in `packages/` with a `PACKAGE.md` and one or more tools; then `python3 make_index.py`, and the new
`index.json` in the same commit. `python3 make_index.py --check` says whether `index.json` is what `packages/` say.

## Licence

AGPL-3.0-only, as SiLVANN's ([`LICENSE`](LICENSE)).
