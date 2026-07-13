# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## What this is

`py1p` is a small Python package that provides a Pythonic wrapper around the
[1Password CLI](https://developer.1password.com/docs/cli/) (`op`). It shells out
to the `op` binary and parses its JSON output into typed Python objects.

The current scope is **read access to Credit Card items** stored in 1Password.
The public API surface is intentionally tiny.

- Package name / distribution: `py1p`
- License: MIT
- Author: Alex Zunega
- Repository: https://github.com/alexzunega/py1p
- Status: Alpha (`Development Status :: 3 - Alpha`)

## Layout

```
.
├── py1p/
│   ├── __init__.py   # public API — re-exports OnePassword
│   └── main.py       # OnePassword and CreditCard implementations
├── setup.py          # setuptools packaging metadata
└── .idea/            # JetBrains/PyCharm project files (not needed to run)
```

Everything of substance lives in `py1p/main.py`. It is currently ~50 lines.

## Public API

`from py1p import OnePassword` is the entry point. `OnePassword` is re-exported
from `main.py` in `py1p/__init__.py`. Keep that re-export in sync when the
public surface changes — anything meant to be public should be importable
directly from `py1p`.

- `OnePassword().credit_cards -> list[CreditCard]`
  Runs `op item list --categories "Credit Card" --format json` and returns one
  `CreditCard` per result. Each `CreditCard` is constructed lazily-per-item by
  fetching its full item detail.
- `CreditCard` exposes read-only properties: `title`, `number`, `expiry`, `cvv`.
  Constructed from an item id via `op item get <id> --format json`.

### How data is parsed

`CreditCard.__init__` fetches the full item JSON and builds
`self._fields = {e['id']: e for e in self._data['fields']}`, keyed by the
1Password field id. Property accessors read specific field ids:
`ccnum`, `expiry`, `cvv`. `title` reads `self._data['title']` directly.

If you add fields (e.g. cardholder name), follow the same pattern: look up the
field id in the `op item get` JSON and add a property that reads from
`self._fields`.

## Requirements & runtime dependencies

- **Python >= 3.12** (declared in `setup.py`; the code uses `list[...]` builtin
  generics as return annotations).
- **No third-party Python dependencies** (`install_requires=[]`). Only the
  standard library (`json`, `subprocess`) is used. Keep it dependency-free
  unless there's a strong reason not to.
- **The `op` CLI must be installed and available on `PATH`**, and the user must
  be signed in / have an active 1Password session. Every operation shells out to
  `op` with `subprocess.run(..., check=True)`, so a missing binary raises
  `FileNotFoundError` and a non-zero exit raises `subprocess.CalledProcessError`.

Because it depends on a real `op` session, this package cannot fully run in an
environment without 1Password configured. When testing logic, mock
`subprocess.run` rather than expecting a live `op`.

## Conventions

- Shell out to `op` via `subprocess.run` with `capture_output=True, text=True,
  check=True`, and always request `--format json`, then `json.loads` the stdout.
  Match this pattern for any new `op` command.
- Keep parsed 1Password JSON in private attributes (`self._data`,
  `self._fields`) and expose values through read-only `@property` accessors.
- This code handles secrets (card numbers, CVVs). Do **not** add logging,
  printing, caching to disk, telemetry, or anything that persists or transmits
  secret values. `__str__` intentionally renders full details for local/interactive
  use only — do not wire it into logs.
- Type-annotate public return values (e.g. `-> list[CreditCard]`).

## Development workflow

There is currently **no test suite, linter config, CI, or build script** in the
repo. If you add tooling, document it here.

Common commands:

```bash
# Install locally for development
pip install -e .

# Smoke test the public API (requires op installed + signed in)
python -c "from py1p import OnePassword; print(OnePassword().credit_cards)"

# Build a distribution (standard setuptools)
python -m build        # or: python setup.py sdist bdist_wheel
```

If you introduce tests, prefer the standard library `unittest` or `pytest`, and
mock `subprocess.run` so tests don't require a live 1Password session.

## Git & contribution notes

- Do not commit secrets or real 1Password item ids/values.
- Keep commit messages short and descriptive (see existing history, e.g.
  "Imports OnePassword to top-level").
- `.idea/` is committed project config for PyCharm; it is not required to build
  or run the package and can be ignored by non-JetBrains users.
