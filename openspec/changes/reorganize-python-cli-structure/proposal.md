# Change: Reorganize Python CLI Project Structure

## Why
The current project structure has all Python files in the root directory, which doesn't follow Python CLI project best practices. This makes the project harder to maintain, test, and distribute properly.

## What Changes
- Create proper `email_classifier/` package directory
- Move all Python modules into package structure
- Add `__init__.py` for proper package exports
- Update setup.py to reference new package structure
- Add `pyproject.toml` for modern Python packaging
- Create proper CLI entry point within package
- Add tests directory structure
- Add configuration for development tools

## Impact
- Affected specs: project-structure
- Affected code: All Python files (classifier.py, cli.py, domains.py, processor.py, reporter.py, ui.py)
- **BREAKING**: Changes import paths for any users importing directly