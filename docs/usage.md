# Usage

This page covers common ways to work with a loaded `confwire.Config`, once
you're already familiar with the concepts in {doc}`configuration`.

## Loading a config file

```python
from confwire import Config

cfg = Config.fromfile("path/to/config.py")  # also accepts .yaml, .yml, .json
```

## Accessing values

Config values are accessible as attributes or dictionary items:

```python
cfg.model.type
cfg["model"]["type"]
```

## Inspecting a config

```python
>>> print(cfg)                # dict-style repr
>>> print(cfg.pretty_text)    # formatted, re-loadable Python source
>>> cfg.filename               # absolute path of the loaded file
>>> cfg.text                   # raw text of the loaded file(s)
```

## Saving a config

```python
cfg.dump("out_config.py")   # format is inferred from the extension
cfg.dump("out_config.yaml")
cfg.dump("out_config.json")
```

## Merging in extra options

`Config.merge_from_dict` applies a flat, dotted-key dictionary on top of an
existing config — handy for applying command-line overrides.

```python
cfg.merge_from_dict({"model.backbone.depth": 101})
```

```{seealso}
{doc}`configuration` for how `_base_` and `_delete_` control merging between
config files, and {doc}`api` for the full method reference.
```
