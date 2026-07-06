# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ConfWire is a lightweight, pure-Python configuration library. It extracts MMCV's config system (inheritance, composition, Python/YAML/JSON loading, dict+attribute access, object construction from `"type"`-tagged dicts) and repackages it as a standalone dependency-light package. `confwire/config.py` still carries the MMCV copyright header — it is closely derived from that codebase.

## Development Commands

The project uses [uv](https://github.com/astral-sh/uv) and requires Python 3.10+.

```bash
uv sync --all-groups          # install runtime + dev + docs deps
pre-commit install            # install git hooks

uv run pytest                 # run all tests
uv run pytest tests -v --cov  # tests with coverage
uv run pytest tests/test_config.py::test_name   # run a single test
uv run pytest -k "pattern"    # run tests matching a name pattern

uv run mypy confwire          # type check (tests/ excluded)
uv run black confwire tests   # format
uv run isort confwire tests   # sort imports
pre-commit run --all-files    # run the full hook suite (black, isort, ruff, mypy, codespell, pyupgrade)
```

Docs are built via console scripts defined in pyproject: `docs-build` and `docs-multiversion` (both in `confwire/_docs.py`, which is excluded from coverage).

## Architecture

The public API is deliberately tiny — `from confwire import Config` is the only export (`confwire/__init__.py`). Four internal modules back it:

- **`confwire/config.py`** (the bulk of the code) — the `Config` class plus `ConfigDict` (an `addict.Dict` subclass that raises `KeyError`/`AttributeError` on missing keys instead of returning empty dicts). Key mechanics to understand before editing:
  - `Config.fromfile()` → `_file2dict()` is the load pipeline. For `.py` configs it copies the file into a temp module, validates syntax, and imports it; YAML/JSON go through `confwire/io.py`.
  - **Inheritance/composition** is driven by special keys: `_base_` (parent config paths, merged via `_merge_a_into_b`), `_delete_` (drop keys from the base rather than merge), `_deprecation_`, and `_args_`. Base variables are substituted in two passes (`_pre_substitute_base_vars` → `_substitute_base_vars`).
  - `merge_from_dict()` supports dotted-key overrides (e.g. `model.backbone.depth`) with `allow_list_keys` handling.
  - `Config` proxies dict + attribute access through `__getattr__`/`__getitem__`/`__setattr__` to an internal `ConfigDict`; `pretty_text` uses yapf to format the config back into Python source.

- **`confwire/build.py`** — `build_from_config()` recursively instantiates Python objects from dicts carrying a `"type"` key (dotted import path). **Security-critical**: `DEFAULT_BLOCKED_TYPES` blocklists dangerous callables (`os.system`, `subprocess.*`, `eval`/`exec`, etc.). Any change here must preserve that blocklist — it prevents arbitrary code execution from config data.

- **`confwire/io.py`** — thin load/dump layer for json/yaml/pickle; format inferred from extension via `FILE_FORMAT_TO_MODE`. Uses libyaml `CLoader`/`CDumper` when available.

- **`confwire/utils/`** — `path.py` (`check_file_exist`), `misc.py` (`import_modules_from_strings`), `version_utils.py` (`digit_version`).

Note: `confwire/config.py` imports `regex as re` on Windows but stdlib `re` elsewhere.

## Conventions

- Line length is 120 across black, isort (black profile), and ruff. Ruff lint selects `E, F, I, W`.
- All functions should carry type hints; mypy runs with `ignore_missing_imports` and excludes `tests/`.
- Branch naming and Conventional Commits are enforced by convention — see CONTRIBUTING.md (`feat/`, `fix/`, `docs/`, `refactor/`, `perf/`, `test/`, `chore/`). PRs target `main`.

## Development Process

Before writing any code, always follow this process:

1. Determine whether the request is:
   - New feature
   - Bug fix
   - Refactor
   - Performance improvement
   - Documentation change

2. Understand the expected behavior.

3. If the acceptance criteria are ambiguous, ask clarifying questions before writing code.

4. Identify:
   - Valid inputs
   - Invalid inputs
   - Boundary cases
   - Expected outputs
   - Expected exceptions
   - Existing behavior that must remain unchanged

5. Produce a concise test plan.

6. Write failing unit tests first (TDD).

7. Verify the tests fail for the expected reason.

8. Implement the smallest possible change to satisfy the tests.

9. Run the affected tests, then the entire test suite.

10. Refactor only after all tests pass.

Never modify behavior without adding or updating tests that describe the intended behavior.

Tests live in `tests/test_*.py` — add cases to the module matching the area under change (`test_config.py`, `test_build.py`, `test_core.py`). Run a single new test with `uv run pytest tests/test_config.py::test_name`, then the full suite with `uv run pytest -v --cov`.

## Repository Notes

- `mmcv/` is a vendored copy of upstream MMCV kept for reference/comparison — it is **not** part of the shipped package (only `confwire/` and `tests/` are packaged per pyproject).
- `test.py` at the root is a scratch/manual file, distinct from the real suite in `tests/`.
