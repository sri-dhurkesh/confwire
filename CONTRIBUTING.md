# Contributing to ConfWire

Thank you for your interest in contributing to ConfWire! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Messages](#commit-messages)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Testing](#testing)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

## Code of Conduct

ConfWire is committed to providing a welcoming and inclusive environment. All contributors are expected to:

- Be respectful and inclusive
- Welcome feedback and different perspectives
- Focus on constructive criticism
- Respect confidentiality and privacy

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/confwire.git
   cd confwire
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   uv sync --all-groups
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Verify the setup:**
   ```bash
   uv run pytest
   ```

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work:

```bash
git checkout -b feat/your-feature-name
# or for bug fixes:
git checkout -b fix/issue-description
```

Branch naming conventions:
- `feat/` - for new features
- `fix/` - for bug fixes
- `docs/` - for documentation updates
- `refactor/` - for code refactoring
- `perf/` - for performance improvements
- `test/` - for test additions
- `chore/` - for maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Add type hints to all functions
- Update docstrings as needed
- Add tests for new functionality

### 3. Run Quality Checks Locally

Before committing, ensure all checks pass:

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Run tests with coverage
uv run pytest tests -v --cov

# Type checking
uv run mypy confwire

# Code formatting
uv run black confwire tests
uv run isort confwire tests
```

### 4. Commit Your Changes

Follow the [Conventional Commits](#commit-messages) specification.

### 5. Push and Open a Pull Request

Push your branch and create a PR against `main`:

```bash
git push origin feat/your-feature-name
```

Then open a pull request on GitHub.

## Commit Messages

ConfWire follows the [Conventional Commits](https://www.conventionalcommits.org/) specification to maintain a clean commit history.

### Format

```
<type>(<scope>)!: <subject>

<body>

<footer>
```

### Type

Must be one of:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Test additions or changes
- **chore**: Build, dependencies, tooling changes
- **ci**: CI/CD configuration changes

### Scope

Optional, but recommended. The scope should specify what is affected:
- Examples: `config`, `builder`, `api`, `docs`, `tests`

### Subject

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize the first letter
- No period (.) at the end
- Limit to 50 characters
- Be descriptive and concise

### Body

Optional, but recommended for non-trivial changes:
- Explain **what** and **why**, not how
- Wrap at 72 characters
- Separate from subject with a blank line

### Footer

Optional. Reference issues or breaking changes:
- Example: `Closes #123`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

```
feat(config): add support for environment variable expansion

Add ability to reference environment variables in config files
using ${ENV_VAR} syntax. This enables dynamic configuration
based on runtime environment.

Closes #45
```

```
fix(builder): handle missing type attribute gracefully

Previously, build_from_config would raise KeyError if 'type' was
not present. Now it returns the dict unchanged, matching expected
behavior for non-buildable values.

Fixes #78
```

```
docs: update installation instructions for Python 3.13
```

## Pull Request Guidelines

### PR Title Format

PR titles must follow Conventional Commits format:
```
<type>(<scope>)!: <description>
```

Examples:
- `feat(config): add YAML anchors support`
- `fix(builder): handle circular references`
- `docs: update API documentation`

### PR Description

Your PR description should:
- **Clearly describe the problem** being solved
- **Explain the solution** and why it was chosen
- **List changes made** in bullet points
- **Reference related issues** (e.g., "Closes #123")
- **Include testing information** - what was tested and how
- **Note any breaking changes** if applicable

### Before Submitting

- [ ] Branch is up-to-date with `main`
- [ ] All tests pass locally (`uv run pytest`)
- [ ] Pre-commit checks pass (`pre-commit run --all-files`)
- [ ] Type checking passes (`uv run mypy confwire`)
- [ ] Code coverage hasn't decreased (aim for 80%+)
- [ ] Documentation is updated if needed
- [ ] Commit messages follow Conventional Commits
- [ ] No unrelated changes in the PR
- [ ] PR description is complete and clear

## Testing

### Writing Tests

- Add tests for all new features in the `tests/` directory
- Follow the existing test structure
- Use descriptive test names: `test_<function>_<scenario>`
- Organize tests in classes for related functionality

### Running Tests

```bash
# Run all tests
uv run pytest tests -v

# Run with coverage
uv run pytest tests -v --cov --cov-report=html

# Run specific test
uv run pytest tests/test_config.py::TestConfig::test_fromfile

# Run tests matching a pattern
uv run pytest tests -k "test_merge"
```

### Coverage Requirements

- Aim for 80%+ code coverage
- New features should include test coverage
- Check coverage report: `uv run coverage report`

## Code Style

ConfWire uses automated tools to enforce consistent code style:

### Tools Used

- **Black** - Code formatting
- **isort** - Import sorting
- **Ruff** - Fast Python linter
- **mypy** - Static type checking

### Running Code Quality Tools

```bash
# Format code
uv run black confwire tests
uv run isort confwire tests

# Check linting
uv run ruff check confwire tests --fix

# Type checking
uv run mypy confwire

# Run all checks (via pre-commit)
pre-commit run --all-files
```

### Guidelines

- **Line length**: 88 characters (enforced by Black)
- **Type hints**: Required for all functions and class methods
- **Imports**: Use `isort` for consistent ordering
- **Docstrings**: Use triple-quoted strings, follow NumPy style
- **Comments**: Keep minimal, explain "why" not "what"

### Type Hints Example

```python
from typing import Any, Dict, Optional

def merge_configs(
    base: Dict[str, Any],
    override: Dict[str, Any],
    allow_new_keys: bool = True,
) -> Dict[str, Any]:
    """Merge override config into base config.

    Args:
        base: The base configuration dictionary.
        override: Configuration values to override.
        allow_new_keys: Whether to allow new keys in override.

    Returns:
        Merged configuration dictionary.
    """
    # Implementation here
    return merged
```

## Documentation

### Updating Documentation

- Update docs if your change affects user-facing behavior
- Keep documentation in sync with code changes
- Use clear, concise language
- Include examples when helpful

### Building Documentation Locally

```bash
# Install docs dependencies
uv sync --group docs

# Build HTML documentation
cd docs
make html

# View in browser
open _build/html/index.html
```

### Documentation Structure

- `docs/index.md` - Overview and quick links
- `docs/getting_started.md` - Setup and first steps
- `docs/installation.md` - Installation instructions
- `docs/configuration.md` - Configuration guide
- `docs/usage.md` - Usage examples
- `docs/api.md` - API reference
- `docs/changelog.md` - Version history

## Reporting Bugs

### How to Report a Bug

1. **Check existing issues** - Search to see if the bug is already reported
2. **Create a detailed issue** including:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version and OS
   - ConfWire version
   - Complete error traceback (if applicable)
   - Any relevant code snippets

### Minimal Reproducible Example

Please include a minimal code example that reproduces the issue:

```python
from confwire import Config

# Example that demonstrates the bug
cfg = Config.fromstring("x = 1", file_format="py")
print(cfg.x)  # Unexpected behavior
```

## Requesting Features

### How to Request a Feature

1. **Check existing issues** - Search to see if it's already requested
2. **Create a feature request** including:
   - Clear description of the desired feature
   - Use case and motivation
   - Example usage (if applicable)
   - Potential implementation approach (optional)
   - Alternative solutions you've considered

### Feature Request Template

```
**Description**
What is the feature you want to add?

**Motivation**
Why do you need this feature? What problem does it solve?

**Example Usage**
How would you like to use this feature?

```python
# Example code showing desired behavior
```

**Additional Context**
Any other relevant information
```

## Questions?

- 📖 Check the [documentation](https://confwire.readthedocs.io/)
- 💬 Open an [issue](https://github.com/sri-dhurkesh/confwire/issues)
- 📧 Contact the maintainers

## Recognition

Contributors to ConfWire are recognized in the project's documentation and release notes. Thank you for helping make ConfWire better!

---

**Happy contributing! 🎉**
