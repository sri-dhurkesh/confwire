# Configuration System

The `Config` class is the core (and currently the only) feature of
`confwire`. It lets you load configuration from **Python**, **YAML**, or
**JSON** files into a single, dict-like object, and it supports composing
configs out of multiple files.

```{note}
`Config` only loads and merges data — it does not build or instantiate
Python objects from that data. Object instantiation is planned for a future
release and is intentionally not covered here.
```

## Loading a config file

Here is the same configuration expressed in each supported format.

`test.py` / `test.yaml` / `test.json`:

:::::{tabs}

::::{tab} Python
```python
a = 1
b = dict(b1=[0, 1, 2], b2=None)
c = (1, 2)
d = "string"
```
::::

::::{tab} YAML
```yaml
a: 1
b:
  b1: [0, 1, 2]
  b2: null
c: [1, 2]
d: string
```
::::

::::{tab} JSON
```json
{
  "a": 1,
  "b": {
    "b1": [0, 1, 2],
    "b2": null
  },
  "c": [1, 2],
  "d": "string"
}
```
::::

:::::

Loading and using the config:

```python
>>> from confwire import Config
>>> cfg = Config.fromfile("test.py")
>>> print(cfg)
dict(a=1, b=dict(b1=[0, 1, 2], b2=None), c=(1, 2), d='string')
>>> cfg.a
1
>>> cfg["b"]["b1"]
[0, 1, 2]
```

```{note}
Native Python tuples (`c = (1, 2)`) are only representable in the Python
config format. YAML and JSON have no tuple type, so the equivalent value is
loaded back as a list (`[1, 2]`).
```

Values can be read using either attribute access (`cfg.a`) or item access
(`cfg["a"]`), since `Config` wraps the underlying data in a dict-like
`ConfigDict`.

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
dict(a=1, b='./work_dir/config_a', c='.py')
```

If you don't want variable substitution, pass
`use_predefined_variables=False` to `Config.fromfile`.

## Config inheritance

Every config format supports inheritance, letting you reuse fields defined
in other config files. Specify a single base with `_base_ = './config_a.py'`
or a list of bases with `_base_ = ['./config_a.py', './config_b.py']`.

The base config used throughout the following examples, `config_a.py`:

:::::{tabs}

::::{tab} Python
```python
a = 1
b = dict(b1=[0, 1, 2], b2=None)
```
::::

::::{tab} YAML
```yaml
a: 1
b:
  b1: [0, 1, 2]
  b2: null
```
::::

::::{tab} JSON
```json
{
  "a": 1,
  "b": {
    "b1": [0, 1, 2],
    "b2": null
  }
}
```
::::

:::::

### Inherit without overlapping keys

`config_b.py` adds new, non-overlapping fields:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./config_a.py"
c = (1, 2)
d = "string"
```
::::

::::{tab} YAML
```yaml
_base_: "./config_a.yaml"
c: [1, 2]
d: string
```
::::

::::{tab} JSON
```json
{
  "_base_": "./config_a.json",
  "c": [1, 2],
  "d": "string"
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_b.py")
>>> print(cfg)
dict(a=1, b=dict(b1=[0, 1, 2], b2=None), c=(1, 2), d='string')
```

New fields in `config_b.py` are combined with the existing fields inherited
from `config_a.py`.

### Inherit with overlapping keys

`config_c.py` overrides part of `b`:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./config_a.py"
b = dict(b2=1)
c = (1, 2)
```
::::

::::{tab} YAML
```yaml
_base_: "./config_a.yaml"
b:
  b2: 1
c: [1, 2]
```
::::

::::{tab} JSON
```json
{
  "_base_": "./config_a.json",
  "b": { "b2": 1 },
  "c": [1, 2]
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_c.py")
>>> print(cfg)
dict(a=1, b=dict(b1=[0, 1, 2], b2=1), c=(1, 2))
```

`b.b2 = None` from `config_a.py` is replaced by `b.b2 = 1` from
`config_c.py`. Keys are merged recursively rather than the whole `b` dict
being overwritten, so `b.b1` is kept unchanged.

### Inherit with ignored fields (`_delete_`)

Sometimes you want a child config to fully replace a nested dict from the
base, instead of merging into it. Set `_delete_=True` inside that dict.

`config_d.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./config_a.py"
b = dict(_delete_=True, b2=None, b3=0.1)
c = (1, 2)
```
::::

::::{tab} YAML
```yaml
_base_: "./config_a.yaml"
b:
  _delete_: true
  b2: null
  b3: 0.1
c: [1, 2]
```
::::

::::{tab} JSON
```json
{
  "_base_": "./config_a.json",
  "b": {
    "_delete_": true,
    "b2": null,
    "b3": 0.1
  },
  "c": [1, 2]
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_d.py")
>>> print(cfg)
dict(a=1, b=dict(b2=None, b3=0.1), c=(1, 2))
```

Because `_delete_=True` is set inside `b`, all old keys (`b1`, `b2`) from
`config_a.py`'s `b` are dropped and replaced entirely by the new `b2`, `b3`
keys. Without `_delete_`, `b1` would have been kept, as in the previous
example.

### Inherit from multiple base configs

Multiple base configs can be combined, as long as they don't define
overlapping top-level keys.

`config_e.py`:

:::::{tabs}

::::{tab} Python
```python
c = (1, 2)
d = "string"
```
::::

::::{tab} YAML
```yaml
c: [1, 2]
d: string
```
::::

::::{tab} JSON
```json
{
  "c": [1, 2],
  "d": "string"
}
```
::::

:::::

`config_f.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = ["./config_a.py", "./config_e.py"]
```
::::

::::{tab} YAML
```yaml
_base_: ["./config_a.yaml", "./config_e.yaml"]
```
::::

::::{tab} JSON
```json
{
  "_base_": ["./config_a.json", "./config_e.json"]
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_f.py")
>>> print(cfg)
dict(a=1, b=dict(b1=[0, 1, 2], b2=None), c=(1, 2), d='string')
```

If two base configs define the same top-level key, `Config.fromfile` raises
a `KeyError` rather than silently picking one.

## Referencing variables from a base config

You can reference a variable defined in a base config using the
`{{ _base_.path.to.value }}` grammar.

`base.py`:

:::::{tabs}

::::{tab} Python
```python
item1 = "a"
item2 = dict(item3="b")
```
::::

::::{tab} YAML
```yaml
item1: a
item2:
  item3: b
```
::::

::::{tab} JSON
```json
{
  "item1": "a",
  "item2": { "item3": "b" }
}
```
::::

:::::

`config_g.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = ["./base.py"]
item = dict(a="{{ _base_.item1 }}", b="{{ _base_.item2.item3 }}")
```
::::

::::{tab} YAML
```yaml
_base_: ["./base.yaml"]
item:
  a: "{{ _base_.item1 }}"
  b: "{{ _base_.item2.item3 }}"
```
::::

::::{tab} JSON
```json
{
  "_base_": ["./base.json"],
  "item": {
    "a": "{{ _base_.item1 }}",
    "b": "{{ _base_.item2.item3 }}"
  }
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./config_g.py")
>>> print(cfg.pretty_text)
item1 = 'a'
item2 = dict(item3='b')
item = dict(a='a', b='b')
```

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

## How a config file is resolved

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

## Next steps

- See {doc}`usage` for common access patterns once a config is loaded.
- See {doc}`api` for the full `Config` API reference.
