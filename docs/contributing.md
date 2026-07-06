# Contributing to ConfWire

For comprehensive contribution guidelines, including development setup, commit message standards, code style requirements, and pull request procedures, please refer to the [CONTRIBUTING.md](https://github.com/sri-dhurkesh/confwire/blob/main/CONTRIBUTING.md) file in the repository root.

This page provides a quick reference for common development tasks.

## Quick Start

### Setting up a development environment

```bash
git clone https://github.com/sri-dhurkesh/confwire.git
cd confwire
uv sync --all-groups
pre-commit install
```

### Running tests

```bash
uv run pytest tests -v --cov
```

### Running code quality checks

```bash
pre-commit run --all-files
uv run mypy confwire
```

### Building the documentation

```bash
uv sync --group docs
cd docs
make html
open _build/html/index.html
```

## Development Workflow

1. Create a feature branch following the naming convention (e.g., `feat/feature-name`, `fix/issue-description`)
2. Make your changes with appropriate tests
3. Ensure all checks pass:
   - `uv run pytest tests -v --cov`
   - `pre-commit run --all-files`
   - `uv run mypy confwire`
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) format
5. Open a pull request with a clear description

## Key Guidelines

- Write tests for new features
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- Maintain 80%+ code coverage
- Use type hints in all functions
- Update documentation if behavior changes

## Need Help?

- See [CONTRIBUTING.md](https://github.com/sri-dhurkesh/confwire/blob/main/CONTRIBUTING.md) for detailed guidelines
- Check the [API documentation](api.md)
- Review [existing issues](https://github.com/sri-dhurkesh/confwire/issues)

Thank you for contributing! 🎉
