# Building Objects

Once you know how to load a config (see {doc}`configuration`), the next step
is turning that configuration into live Python objects. `confwire` does this
with a single function, `build_from_config`.

```{note}
This section builds on the {doc}`tutorial <getting_started>`. Everything
here assumes you already have a config dictionary — whether hand-written or
loaded from a file via `Config.fromfile`.
```

## The idea

A config dictionary describes *what* to build using a special `"type"` key
holding a dotted import path. Every other key becomes a keyword argument to
that callable.

```python
>>> from confwire import build_from_config
>>> cfg = {"type": "urllib.request.Request", "url": "https://example.com", "method": "GET"}
>>> req = build_from_config(cfg)
>>> req.full_url, req.method
('https://example.com', 'GET')
```

`confwire` imports `urllib.request.Request`, then calls it as
`Request(url="https://example.com", method="GET")`.

A dict *without* a `"type"` key is treated as plain data and returned
unchanged:

```python
>>> build_from_config({"a": 1, "b": 2})
{'a': 1, 'b': 2}
```

## Nested objects

Any value that is itself a `"type"`-tagged dict is built first, then passed
to its parent. This works at any depth:

```python
config = {
    "type": "myproject.models.Detector",
    "backbone": {
        "type": "myproject.models.ResNet",
        "depth": 50,
    },
    "num_classes": 80,
}

detector = build_from_config(config)
# Equivalent to:
#   Detector(backbone=ResNet(depth=50), num_classes=80)
```

## Relative type paths

If a `"type"` starts with a dot, it is resolved relative to `base_package`:

```python
build_from_config(
    {"type": ".models.ResNet", "depth": 50},
    base_package="myproject",
)
```

Passing a relative type without a `base_package` raises `ImportError`.

## From a config file

`build_from_config` pairs naturally with `Config.fromfile`:

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
>>> cfg = Config.fromfile("model.py")
>>> req = build_from_config(cfg["request"])
>>> req.full_url, req.method
('https://example.com', 'GET')
```

## Safety: blocked types

Some import paths allow arbitrary code or command execution and are **never**
built, regardless of your configuration:

```python
>>> build_from_config({"type": "os.system", "command": "rm -rf /"})
Traceback (most recent call last):
    ...
PermissionError: Building objects of type 'os.system' is not allowed.
```

The default blocklist ({data}`confwire.build.DEFAULT_BLOCKED_TYPES`) covers
three categories of dangerous calls:

- **Process/command execution** — `os.system`, `os.popen`, `os.execv`,
  `os.execve`, `os.execvp`, `os.execvpe`, `os.spawnl`, `os.spawnv`,
  `subprocess.Popen`, `subprocess.call`, `subprocess.run`,
  `subprocess.check_call`, `subprocess.check_output`
- **File/directory removal** — `os.remove`, `os.unlink`, `os.rmdir`,
  `shutil.rmtree`
- **Arbitrary code execution** — `eval`, `exec`, `builtins.eval`,
  `builtins.exec`

You can supply your own set via the `blocked_types` argument to override the
default — note that this *replaces* the default blocklist rather than
extending it, so include any of the entries above that you still want
blocked.

```{seealso}
The {doc}`api` reference documents `build_from_config` and `build_value` in
full.
```
