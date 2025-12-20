## ADDED Requirements

### Requirement: Python Package Structure
The project SHALL follow Python CLI project best practices with proper package directory structure.

#### Scenario: Package installation
- **WHEN** user runs `pip install -e .`
- **THEN** the package installs correctly with all modules accessible

#### Scenario: CLI command execution
- **WHEN** user runs `email-classifier --help`
- **THEN** the CLI tool works correctly from the installed package

#### Scenario: Python imports
- **WHEN** user runs `from email_classifier import EmailClassifier`
- **THEN** the import works correctly and all classes are accessible

### Requirement: Modern Python Packaging
The project SHALL use modern Python packaging with pyproject.toml configuration.

#### Scenario: Build system configuration
- **WHEN** pyproject.toml is present
- **THEN** the project uses modern build tools and follows PEP 517/518

#### Scenario: Development dependencies
- **WHEN** installing with `pip install -e ".[dev]"`
- **THEN** all development tools are available

### Requirement: Development Infrastructure
The project SHALL include proper development infrastructure with tests and tooling configuration.

#### Scenario: Test execution
- **WHEN** running `pytest`
- **THEN** all tests execute and pass

#### Scenario: Code formatting
- **WHEN** running `black .` and `isort .`
- **THEN** code is formatted according to project standards

#### Scenario: Type checking
- **WHEN** running `mypy email_classifier`
- **THEN** type checking completes without critical errors

## MODIFIED Requirements

### Requirement: Project Layout
The project SHALL organize code in a proper Python package structure under `email_classifier/` directory.

#### Scenario: Module organization
- **WHEN** viewing the project structure
- **THEN** all Python modules are under `email_classifier/` package
- **AND** `__init__.py` provides clean public API exports

#### Scenario: Entry point configuration
- **WHEN** checking setup.py entry points
- **THEN** CLI entry point references the new package structure
- **AND** console script works after installation