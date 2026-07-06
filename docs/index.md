# confwire

A lightweight, Hydra-inspired alternative for instantiating nested Python
objects from Python-style config files, with type-validated construction and
precise, path-qualified error messages.

`confwire` gives you two things:

1. A **`Config`** class for loading, composing, and manipulating
   configuration from Python, YAML, or JSON files — with dict-like access,
   inheritance, variable substitution, and deprecation warnings.
2. A **`build_from_config`** function for turning a `"type"`-tagged config
   tree into live Python objects.

Start with the tutorial to learn how configs work, then move on to building
objects.

## Tutorial

```{toctree}
:maxdepth: 2

installation
getting_started
configuration
build
advanced
```

## Reference

```{toctree}
:maxdepth: 2

api
contributing
changelog
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
