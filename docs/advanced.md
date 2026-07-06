# Advanced Configuration

This page covers features beyond the core tutorial in {doc}`configuration`:
common usage patterns, predefined path variables, deprecating a config
file, and how config resolution works internally.

## Usage

Common ways to work with a loaded `confwire.Config`, once you're already
familiar with the concepts in {doc}`configuration`.

### Loading a config file

```python
from confwire import Config

cfg = Config.fromfile("path/to/config.py")  # also accepts .yaml, .yml, .json
```

### Accessing values

Config values are accessible as attributes or dictionary items:

```python
cfg.b.b1
cfg["b"]["b1"]
```

### Inspecting a config

```python
>>> print(cfg)                # "Config (path: ...): {...}" repr
>>> print(cfg.pretty_text)    # formatted, re-loadable Python source
>>> cfg.filename               # absolute path of the loaded file
>>> cfg.text                   # raw text of the loaded file(s)
```

### Saving a config

```python
cfg.dump("out_config.py")   # format is inferred from the extension
cfg.dump("out_config.yaml")
cfg.dump("out_config.json")
```

### Merging in extra options

`Config.merge_from_dict` applies a flat, dotted-key dictionary on top of an
existing config — handy for applying command-line overrides.

```python
>>> cfg.merge_from_dict({"b.b1.b11": 101})
>>> cfg.b.b1.b11
101
```

```{seealso}
{doc}`configuration` for how `_base_` and `_delete_` control merging between
config files, and {doc}`api` for the full method reference.
```

## Predefined variables

Every config format supports a small set of predefined variables that are
substituted with real values before the file is parsed. Write them as
`{{ variable_name }}`.

| Variable                       | Description                                          | Example                                         |
| ------------------------------- | ----------------------------------------------------- | ------------------------------------------------ |
| `{{ fileDirname }}`             | Directory of the config file being loaded              | `/home/user/project/configs`                     |
| `{{ fileBasename }}`            | Basename of the config file, with extension            | `config_a.py`                                    |
| `{{ fileBasenameNoExtension }}` | Basename of the config file, without extension         | `config_a`                                       |
| `{{ fileExtname }}`             | Extension of the config file                           | `.py`                                            |

These names mirror the [VS Code variables reference](https://code.visualstudio.com/docs/editor/variables-reference).

`config_a.py`:

:::::{tabs}

::::{tab} Python
```python
a = 1
b = "./work_dir/{{ fileBasenameNoExtension }}"
c = "{{ fileExtname }}"
```
::::

::::{tab} YAML
```yaml
a: 1
b: "./work_dir/{{ fileBasenameNoExtension }}"
c: "{{ fileExtname }}"
```
::::

::::{tab} JSON
```json
{
  "a": 1,
  "b": "./work_dir/{{ fileBasenameNoExtension }}",
  "c": "{{ fileExtname }}"
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_a.py")
>>> print(cfg)
Config (path: ./config_a.py): {'a': 1, 'b': './work_dir/config_a', 'c': '.py'}
```

If you don't want variable substitution, pass
`use_predefined_variables=False` to `Config.fromfile`.

## Deprecating a config file

You can mark a config file as deprecated. Loading it triggers a
`DeprecationWarning` pointing users at its replacement.

`deprecated_cfg.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = "expected_cfg.py"

_deprecation_ = dict(
    expected="expected_cfg.py",  # optional: shown in the warning
    reference="https://github.com/your-org/your-repo/pull/123",  # optional
)
```
::::

::::{tab} YAML
```yaml
_base_: expected_cfg.yaml

_deprecation_:
  expected: expected_cfg.yaml
  reference: "https://github.com/your-org/your-repo/pull/123"
```
::::

::::{tab} JSON
```json
{
  "_base_": "expected_cfg.json",
  "_deprecation_": {
    "expected": "expected_cfg.json",
    "reference": "https://github.com/your-org/your-repo/pull/123"
  }
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./deprecated_cfg.py")
DeprecationWarning: The config file deprecated_cfg.py will be deprecated in
the future. Please use expected_cfg.py instead. More information can be
found at https://github.com/your-org/your-repo/pull/123
```

## Additional notes

:::::{tabs}

::::{tab} How a config file is resolved
The diagram below summarizes what happens inside `Config.fromfile`:

```text
Config.fromfile(path)
        │
        ▼
 substitute predefined variables ({{ fileBasename }}, ...)
        │
        ▼
 parse file (Python exec / YAML / JSON)
        │
        ▼
 has "_deprecation_" key? ──yes──▶ emit DeprecationWarning
        │ no
        ▼
 has "_base_" key? ──no──▶ done, wrap result in Config
        │ yes
        ▼
 recursively load each base file (same steps as above)
        │
        ▼
 substitute "{{ _base_.* }}" references using loaded base values
        │
        ▼
 merge this file's fields into the merged base fields
 (dict fields merge recursively; "_delete_: true" replaces instead)
        │
        ▼
 return final Config
```
::::

:::::

## Next steps

- See {doc}`build` to turn a config into live Python objects.
- See {doc}`api` for the full `Config` API reference.
