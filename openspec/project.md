# Project Context

## Purpose
Email Domain Classifier is a Python library for classifying emails by domain using dual-method validation. It processes large CSV datasets efficiently with streaming processing and provides beautiful terminal output. The system combines keyword taxonomy matching and structural template analysis for accurate domain classification across 10 business domains (Finance, Technology, Retail, Logistics, Healthcare, Government, HR, Telecommunications, Social Media, Education).

## Tech Stack
- **Python 3.10+** - Core programming language
- **Rich 13.0.0+** - Terminal UI with progress bars, tables, and panels
- **Standard Library** - csv, re, logging, pathlib, dataclasses, collections
- **Development Tools** - pytest, black, isort, mypy (optional dev dependencies)

## Project Conventions

### Code Style
- **Python PEP 8** compliance with 4-space indentation
- **Type hints** using dataclasses and typing module
- **Docstrings** following Google/NumPy style conventions
- **Descriptive variable names** with snake_case
- **Class names** in PascalCase
- **Constants** in UPPER_SNAKE_CASE
- **Line length** target ~88 characters (Black default)

### Architecture Patterns
- **Modular package structure** with single responsibility per module
- **Dataclass patterns** for data structures and configuration
- **Strategy pattern** for dual classification methods
- **Factory pattern** for creating classifiers and processors
- **Streaming processing** for memory-efficient large dataset handling
- **Dependency injection** for testable components

### Testing Strategy
- **Unit tests** for individual classification methods
- **Integration tests** for end-to-end processing workflows
- **Mock data** using sample_emails.csv for consistent testing
- **Coverage reporting** with pytest-cov
- **Type checking** with mypy for static analysis

### Git Workflow
- **Feature branches** for new functionality
- **Descriptive commit messages** following conventional commits
- **Pull requests** for code review and collaboration
- **Semantic versioning** for releases (currently v1.0.0)

## Domain Context

### Email Classification Domains
The system classifies emails into 10 business domains:
- **Finance** (💰) - Banking, payments, financial services
- **Technology** (💻) - Software, hardware, IT services
- **Retail** (🛒) - E-commerce, shopping, consumer goods
- **Logistics** (📦) - Shipping, supply chain, transportation
- **Healthcare** (🏥) - Medical services, health insurance
- **Government** (🏛️) - Public sector, regulatory agencies
- **HR** (👥) - Human resources, recruitment, employee services
- **Telecommunications** (📞) - Phone, internet, communication services
- **Social Media** (📱) - Social platforms, networking services
- **Education** (🎓) - Schools, universities, learning platforms

### Dual-Method Validation
Classification requires agreement between:
1. **Keyword Taxonomy Matching** - Domain-specific keywords, sender patterns, subject patterns
2. **Structural Template Matching** - Email structure, formality, greeting/signature patterns

### Input Data Format
CSV files with columns: sender, receiver, timestamp, subject, body, has_url

## Important Constraints
- **Memory efficiency** - Must handle large datasets (>100K emails) via streaming
- **Processing speed** - Optimized for batch processing with configurable chunk sizes
- **Classification accuracy** - Dual validation reduces false positives
- **Cross-platform compatibility** - Works on Windows, macOS, Linux
- **Python version compatibility** - Supports Python 3.10+

## External Dependencies
- **Rich Library** - Terminal UI components for progress bars and tables
- **Standard Python Library** - No external APIs or services required
- **File System** - Local CSV file input/output processing
- **Logging System** - Built-in Python logging for debugging and auditing
