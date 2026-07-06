## Description
Adds AI coding-assistant guidance (`CLAUDE.md`) and bumps the line length from 88 to 120 across black, isort, and ruff.

## Type of Change
- [ ] Documentation update
- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring

## Changes Made
- Added `CLAUDE.md` with project overview, dev commands, architecture, and a test-driven development process.
- Set line length to 120 in `pyproject.toml` (black, isort, ruff).

## Testing
- [x] All existing tests pass

### Test Commands
```bash
uv run pytest -v --cov
pre-commit run --all-files
```

## Documentation
- [x] Updated documentation (added `CLAUDE.md`)

## Code Quality Checklist
- [x] All linting checks pass (`pre-commit run --all-files`)
- [x] No breaking changes to the public API
