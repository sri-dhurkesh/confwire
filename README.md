<p align="center">
  <img src="assets/confwire_logo_lime_emerald.svg" alt="ConfWire logo" width="100%">
</p>

# ConfWire

**ConfWire** is a lightweight Python configuration library that makes application configuration simple, flexible, and Pythonic.

It supports native Python, YAML, and JSON configuration files while providing powerful configuration composition without the heavy dependencies of MMCV.

<p align="center">
  <a href="https://pypi.org/project/confwire/"><img src="https://img.shields.io/pypi/v/confwire.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/confwire/"><img src="https://img.shields.io/pypi/pyversions/confwire.svg" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/sri-dhurkesh/confwire.svg" alt="License"></a>
  <a href="https://github.com/sri-dhurkesh/confwire/actions"><img src="https://img.shields.io/github/actions/workflow/status/sri-dhurkesh/confwire/test.yml?branch=main&label=build" alt="Build Status"></a>
  <a href="https://github.com/sri-dhurkesh/confwire/actions"><img src="https://img.shields.io/github/actions/workflow/status/sri-dhurkesh/confwire/test.yml?branch=main&label=tests" alt="Tests"></a>
  <a href="https://github.com/sri-dhurkesh/confwire"><img src="https://img.shields.io/codecov/c/github/sri-dhurkesh/confwire" alt="Coverage"></a>
  <br>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/lint-ruff-black.svg" alt="Ruff"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <a href="https://github.com/python/mypy"><img src="https://img.shields.io/badge/type%20checked-mypy-blue.svg" alt="MyPy"></a>
  <a href="https://confwire.readthedocs.io/en/latest/"><img src="https://img.shields.io/badge/docs-readthedocs-blue.svg" alt="Documentation"></a>
  <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg" alt="Pre-commit"></a>
  <a href="https://pypi.org/project/confwire/"><img src="https://img.shields.io/pypi/dm/confwire.svg" alt="Downloads"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#why-confwire">Why ConfWire?</a> •
  <a href="#features">Features</a> •
  <a href="#comparison-with-mmcv-config">Comparison</a> •
  <a href="#configuration-examples">Examples</a> •
  <a href="#api-reference">API</a> •
  <a href="#documentation">Docs</a>
</p>

---

## Installation

Using pip:

```bash
pip install confwire
```

Using [uv](https://github.com/astral-sh/uv):

```bash
uv add confwire
```

ConfWire requires Python 3.10+.

---

## Quick Start

```python
from confwire import Config

cfg = Config.fromfile("config.py")

print(cfg.server.port)      # attribute-style access
print(cfg["server"]["port"])  # dict-style access
```

---

## Why ConfWire?

Most Python projects eventually need more than a single flat config file: different environments, experiment variants, or shared defaults that get overridden in specific cases. Reimplementing this composition and inheritance logic by hand is tedious and error-prone.

ConfWire solves this by providing a small, self-contained `Config` object that:

- Loads Python, YAML, or JSON files interchangeably
- Merges configs together through `_base_` inheritance
- Preserves dict-like and attribute-like access (`cfg.server.port` and `cfg["server"]["port"]` both work)
- Lets you build actual Python objects straight from configuration data

It is designed to be dropped into any project, not tied to a specific framework or domain.

---

## Features

- **Native Python configuration files** — write configs as plain `.py` files with regular variables and dicts
- **YAML configuration support** — load and dump `.yaml` / `.yml` files
- **JSON configuration support** — load and dump `.json` files
- **Configuration inheritance** — extend one or more base configs with `_base_`
- **Configuration composition** — merge multiple config files into a single, unified config
- **Importing configurations from other files** — reference and combine configs across your project
- **Native Python imports inside configuration files** — use real Python code, functions, and imports in `.py` configs
- **Object construction from config** — build nested Python objects directly from `"type"`-tagged dictionaries, with a built-in blocklist for dangerous types
- **Simple API** — a single `Config` class covers loading, merging, and dumping
- **Zero unnecessary dependencies** — no deep learning frameworks or unrelated tooling required
- **Lightweight installation** — install in seconds, use in any Python project
- **Easy integration** — drop it into an existing project without restructuring anything

---

## Comparison with MMCV Config

ConfWire's `Config` system is heavily inspired by [MMCV](https://github.com/open-mmlab/mmcv)'s configuration module, which is well designed but only available as part of the full MMCV package.

| | MMCV Config | ConfWire |
|---|---|---|
| Config inheritance & composition | ✅ | ✅ |
| Python / YAML / JSON configs | ✅ | ✅ |
| Dict + attribute-style access | ✅ | ✅ |
| Standalone install | ❌ (requires the MMCV ecosystem) | ✅ |
| Dependencies | Large (CUDA/vision-oriented stack) | Minimal, pure-Python |
| Usable outside computer vision projects | Limited | Yes, general purpose |

ConfWire extracts the parts of MMCV's config system that are broadly useful and repackages them as a small, independent library — without requiring MMCV itself.

---

## Configuration Examples

### Loading Configurations

`Config.fromfile()` automatically infers the file format from its extension. Supported formats: `.py`, `.yaml` / `.yml`, and `.json`.

```python
from confwire import Config

cfg = Config.fromfile("configs/app.py")
cfg = Config.fromfile("configs/app.yaml")
cfg = Config.fromfile("configs/app.json")
```

You can also inspect and export a loaded config:

```python
cfg.filename      # absolute path to the source file
cfg.text          # raw text of the config file(s)
cfg.pretty_text   # formatted Python-style representation
cfg.dump("out.yaml")  # write the config back out, format inferred from extension
```

### Python Configuration Example

`config.py`:

```python
server = dict(
    host="0.0.0.0",
    port=8080,
)
database = dict(
    driver="postgresql",
    pool_size=10,
)
```

```python
from confwire import Config

cfg = Config.fromfile("config.py")
print(cfg.server.port)      # 8080
print(cfg.database.driver)  # postgresql
```

Since these are plain Python files, you can use native Python imports and logic directly inside a config:

```python
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")

logging = dict(
    level=log_level,
    format="%(asctime)s %(levelname)s %(message)s",
)
```

### YAML Example

`config.yaml`:

```yaml
server:
  host: 0.0.0.0
  port: 8080
database:
  driver: postgresql
  pool_size: 10
```

```python
from confwire import Config

cfg = Config.fromfile("config.yaml")
print(cfg.server.port)  # 8080
```

### JSON Example

`config.json`:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080
  },
  "database": {
    "driver": "postgresql",
    "pool_size": 10
  }
}
```

```python
from confwire import Config

cfg = Config.fromfile("config.json")
print(cfg.server.port)  # 8080
```

### Configuration Inheritance Example

A config can extend one or more base configs using the reserved `_base_` key. Values defined in the child config override matching values from the base config(s).

`base.py`:

```python
server = dict(
    host="0.0.0.0",
    port=8080,
)
database = dict(
    driver="postgresql",
    pool_size=10,
)
```

`production.py`:

```python
_base_ = "./base.py"

database = dict(pool_size=50)  # overrides only database.pool_size
```

```python
from confwire import Config

cfg = Config.fromfile("production.py")
print(cfg.server.port)         # 8080 (inherited from base.py)
print(cfg.database.pool_size)  # 50 (overridden)
```

`_base_` also accepts a list of files, letting you compose a config out of several base files at once:

```python
_base_ = ["./server.py", "./database.yaml", "./logging.json"]
```

To fully replace a base value instead of merging into it, set `_delete_=True` on the overriding dict:

```python
database = dict(_delete_=True, driver="sqlite")
```

---

## API Reference

### `Config`

| Member | Description |
|---|---|
| `Config.fromfile(filename)` | Load a config from a `.py`, `.yaml`/`.yml`, or `.json` file, resolving `_base_` inheritance. |
| `Config.fromstring(cfg_str, file_format)` | Build a config from an in-memory string, given its intended file format. |
| `cfg.filename` | Absolute path of the loaded file. |
| `cfg.text` | Raw source text of the config (including merged base files). |
| `cfg.pretty_text` | Formatted, Python-style string representation of the config. |
| `cfg.dump(file=None)` | Write the config to a file, or return it as a string if no file is given. |
| `cfg.merge_from_dict(options)` | Merge a flat, dot-separated key/value dict into the config. |

Configs support both attribute access (`cfg.server.port`) and item access (`cfg["server"]["port"]`).

### `confwire.build`

| Member | Description |
|---|---|
| `build_from_config(config_dict, base_package=None, blocked_types=None)` | Build a Python object from a `"type"`-tagged dict, recursively building any nested dicts that also contain a `"type"` key. |
| `build_value(value, base_package=None, blocked_types=None)` | Recursively resolve buildable objects nested inside a value (dict, list, etc.). |

```python
from confwire.build import build_from_config

instance = build_from_config({
    "type": "botocore.config.Config",
    "region_name": "us-east-1",
})
```

A default blocklist prevents `"type"` values that would allow arbitrary code or command execution (e.g. `os.system`, `subprocess.run`, `eval`) from being built.

---

## Documentation

Full documentation, including guides and the complete API reference, is available at [confwire.readthedocs.io](https://confwire.readthedocs.io/en/latest/).

---

## Contributing

Contributions are welcome. To get started:

```bash
git clone https://github.com/sri-dhurkesh/confwire.git
cd confwire
uv sync --all-groups
pre-commit install
pytest
```

Please open an issue to discuss significant changes before submitting a pull request.

---

## License

ConfWire is released under the [Apache License 2.0](LICENSE).
