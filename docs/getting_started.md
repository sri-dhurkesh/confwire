# Getting Started

This page gives a quick overview of what `confwire` does today and how to
start using it in your project.

## What is confwire?

`confwire` gives you a single `Config` class for loading structured
configuration from **Python**, **YAML**, or **JSON** files. It supports:

- dict-like access to config values (attribute and item access)
- config inheritance across multiple files (`_base_`)
- overriding vs. merging of nested fields (`_delete_`)
- predefined path variables (`{{ fileBasename }}`, etc.)
- referencing values defined in a base config
- deprecation warnings for retired config files

```{note}
`confwire` does not yet build or instantiate Python objects from config
values — it only loads and manipulates the configuration data itself.
```

## A minimal example

`test.py`:

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

Loading it:

```python
>>> from confwire import Config
>>> cfg = Config.fromfile("test.py")
>>> print(cfg)
dict(a=1, b=dict(b1=[0, 1, 2], b2=None), c=(1, 2), d='string')
```

## Next steps

- Follow the {doc}`installation` guide to install the package.
- Read {doc}`configuration` for a full tour of the config system, including
  inheritance, variable substitution, and deprecation.
- Read {doc}`usage` for common access patterns.
- Browse the {doc}`api` reference for detailed documentation of every
  public class and function.
