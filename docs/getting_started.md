# Getting Started

This page gives a quick overview of what `confwire` does today and how to
start using it in your project.

## What is confwire?

`confwire` helps you build and manage lightweight configuration files using
native **Python**, **YAML**, or **JSON** — pick whichever format suits you.
Once loaded, you can also use that same configuration to build Python
objects directly, making it easy to go from config to working code.

## A minimal example

### Loading a configuration file

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
Config (path: test.py): {'a': 1, 'b': {'b1': [0, 1, 2], 'b2': None}, 'c': (1, 2), 'd': 'string'}
```

Values can be read using either attribute access or item access, and nested
values are reached the same way at any depth:

```python
>>> cfg.a
1
>>> cfg.b.b1
[0, 1, 2]
>>> cfg["b"]["b1"]
[0, 1, 2]
```

### Creating an object

A config dict can also describe a Python object to build, using a `"type"`
key holding a dotted import path. Every other key becomes a keyword argument.

`object.py`:

:::::{tabs}

::::{tab} Python
```python
request = dict(
    type="urllib.request.Request",
    url="https://example.com",
    method="GET",
)
```
::::

::::{tab} YAML
```yaml
request:
  type: urllib.request.Request
  url: https://example.com
  method: GET
```
::::

::::{tab} JSON
```json
{
  "request": {
    "type": "urllib.request.Request",
    "url": "https://example.com",
    "method": "GET"
  }
}
```
::::

:::::

```python
>>> from confwire import Config, build_from_config
>>> cfg = Config.fromfile("object.py")
>>> req = build_from_config(cfg.request)
>>> req.full_url, req.method
('https://example.com', 'GET')
```

```{seealso}
{doc}`build` for nested objects, relative type paths, and the safety
blocklist.
```

## Next steps

- Follow the {doc}`installation` guide to install the package.
- Read {doc}`configuration` for a full tour of the config system, including
  inheritance, variable substitution, and deprecation.
- Read {doc}`build` to turn a config into live Python objects.
- Read {doc}`advanced` for common usage patterns and other advanced topics.
- Browse the {doc}`api` reference for detailed documentation of every
  public class and function.
