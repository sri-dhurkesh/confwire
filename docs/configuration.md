# Config

The `Config` class is the core (and currently the only) feature of
`confwire`. It lets you load configuration from **Python**, **YAML**, or
**JSON** files into a single, dict-like object, and it supports composing
configs out of multiple files.

```{note}
`Config` only loads and merges data. Turning that data into live Python
objects is handled separately by `build_from_config` — see {doc}`build`.
```

## Reserved keys

```{warning}
`_base_`, `_delete_`, `_deprecation_`, `_args_`, `filename`, `text`, and
`pretty_text` are reserved and must not be used as your own config keys.
```

## 1. Loading a configuration file

```{note}
The examples on this page use plain, abstract key names (`a`, `b`, `c`, ...)
on purpose, rather than domain-specific ones like `model` or `backbone` —
`confwire` isn't tied to machine learning or any other specific use case,
and generic names make the mechanics easier to follow.
```

Real configs are usually nested, several levels deep — think of it like a
small matrix, where `b` has children `b1` and `b2`, and `b1` itself has
children `b11` and `b12`. Here is one such config, expressed in each
supported format.

`train.py` / `train.yaml` / `train.json`:

:::::{tabs}

::::{tab} Python
```python
a = 1
b = dict(
    b1=dict(b11=10, b12=20),
    b2=30,
)
c = "string"
```
::::

::::{tab} YAML
```yaml
a: 1
b:
  b1:
    b11: 10
    b12: 20
  b2: 30
c: string
```
::::

::::{tab} JSON
```json
{
  "a": 1,
  "b": {
    "b1": { "b11": 10, "b12": 20 },
    "b2": 30
  },
  "c": "string"
}
```
::::

:::::

Load it, then reach any nested value with the dot operator — no matter how
deep it is:

```python
>>> from confwire import Config
>>> cfg = Config.fromfile("train.py")
>>> print(cfg)
Config (path: train.py): {'a': 1, 'b': {'b1': {'b11': 10, 'b12': 20}, 'b2': 30}, 'c': 'string'}
>>> cfg.a
1
>>> cfg.b.b1.b11
10
>>> cfg.b.b1.b12
20
>>> cfg.b.b2
30
```

Item access works the same way, and both styles can be mixed:

```python
>>> cfg["b"]["b1"]["b11"]
10
>>> cfg.b["b1"].b12
20
```

Values can be read using either attribute access (`cfg.a`) or item access
(`cfg["a"]`), since `Config` wraps the underlying data in a dict-like
`ConfigDict`.

## 2. Composing configs with `_base_`

As a project grows, a single config file gets unwieldy. `confwire` lets you
split shared settings into a base file and reuse them from as many child
configs as you like, via `_base_ = './other_config.py'` (or a list of
files).

Move the `b` block from the previous example into its own file, `base.py`:

:::::{tabs}

::::{tab} Python
```python
b = dict(
    b1=dict(b11=10, b12=20),
    b2=30,
)
```
::::

::::{tab} YAML
```yaml
b:
  b1:
    b11: 10
    b12: 20
  b2: 30
```
::::

::::{tab} JSON
```json
{
  "b": {
    "b1": { "b11": 10, "b12": 20 },
    "b2": 30
  }
}
```
::::

:::::

Then `full.py` inherits it and only adds what's new:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./base.py"
a = 1
c = "string"
```
::::

::::{tab} YAML
```yaml
_base_: "./base.yaml"
a: 1
c: string
```
::::

::::{tab} JSON
```json
{
  "_base_": "./base.json",
  "a": 1,
  "c": "string"
}
```
::::

:::::

Loading `full.py` alone gives you back the exact same merged config as
before — `confwire` pulls in everything from `base.py` automatically:

```python
>>> cfg = Config.fromfile("./full.py")
>>> print(cfg)
Config (path: ./full.py): {'b': {'b1': {'b11': 10, 'b12': 20}, 'b2': 30}, 'a': 1, 'c': 'string'}
```

If two base configs define the same top-level key, `Config.fromfile` raises
a `KeyError` rather than silently picking one.

## 3. Overriding with `_delete_`

By default, a child config *merges* into the base recursively — a nested
dict field is combined key by key, not replaced wholesale. Sometimes you
want a full replacement instead, e.g. swapping `b` for a completely
different shape. Set `_delete_=True` inside the dict you want to replace
outright.

`override.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./base.py"
b = dict(_delete_=True, b3=99, b4=100)
```
::::

::::{tab} YAML
```yaml
_base_: "./base.yaml"
b:
  _delete_: true
  b3: 99
  b4: 100
```
::::

::::{tab} JSON
```json
{
  "_base_": "./base.json",
  "b": {
    "_delete_": true,
    "b3": 99,
    "b4": 100
  }
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./override.py")
>>> print(cfg)
Config (path: ./override.py): {'b': {'b3': 99, 'b4': 100}}
```

Because `_delete_=True` is set inside `b`, the entire `b` dict from
`base.py` — `b1`, `b2`, everything — is dropped and replaced by the new
`b3`, `b4` fields. Without `_delete_`, `b1` and `b2` would have merged in
alongside the new `b3` key instead.

## 4. Referencing values

### Referencing within the same file

Since a Python config file is executed as real Python, one variable can
simply reference another defined earlier in the same file — no special
syntax needed. This only works for the **Python** format; YAML and JSON have
no notion of executing code, so this pattern is Python-only.

```python
x = 1
y = dict(z=x)
```

```python
>>> cfg = Config.fromfile("./sameref.py")
>>> print(cfg)
Config (path: ./sameref.py): {'x': 1, 'y': {'z': 1}}
```

### Referencing values from a base file

To pull a value from a *base* config into a child config — across all three
formats — use the `{{ _base_.path.to.value }}` grammar. Write the
placeholder without surrounding quotes; `confwire` substitutes it with the
real value (including its type) before the file is parsed.

`value.py`:

:::::{tabs}

::::{tab} Python
```python
n = 5
```
::::

::::{tab} YAML
```yaml
n: 5
```
::::

::::{tab} JSON
```json
{
  "n": 5
}
```
::::

:::::

`ref.py`:

:::::{tabs}

::::{tab} Python
```python
_base_ = "./value.py"
m = dict(x={{ _base_.n }})
```
::::

::::{tab} YAML
```yaml
_base_: "./value.yaml"
m:
  x: {{ _base_.n }}
```
::::

::::{tab} JSON
```text
{
  "_base_": "./value.json",
  "m": {
    "x": {{ _base_.n }}
  }
}
```
::::

:::::

```python
>>> cfg = Config.fromfile("./ref.py")
>>> print(cfg)
Config (path: ./ref.py): {'n': 5, 'm': {'x': 5}}
```

```{warning}
Do **not** wrap the placeholder in quotes (`"{{ _base_.x }}"`). The
substitution already inserts the value with correct quoting for its type,
so adding your own quotes produces invalid Python/YAML/JSON.
```

## Next steps

- See {doc}`advanced` for common usage patterns, predefined path variables,
  deprecating a config file, and how config resolution works internally.
- See {doc}`api` for the full `Config` API reference.
