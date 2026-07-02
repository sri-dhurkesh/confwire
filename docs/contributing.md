# Contributing

Contributions to `confwire` are welcome!

## Setting up a development environment

```bash
git clone https://github.com/sri-dhurkesh/confwire.git
cd confwire
uv sync --group docs
```

## Running tests

```bash
uv run pytest
```

## Building the documentation

```bash
cd docs
make html
```

## Submitting changes

1. Fork the repository and create a feature branch.
2. Make your changes, with tests where applicable.
3. Open a pull request describing the change and its motivation.
