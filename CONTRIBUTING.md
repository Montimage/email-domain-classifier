# Contributing to Email Domain Classifier

Thank you for your interest in contributing to the Email Domain Classifier project! This guide will help you get started with contributing code, documentation, or ideas.

## 🚀 Quick Start

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Set up** your development environment
4. **Create** a feature branch
5. **Make** your changes
6. **Test** thoroughly
7. **Submit** a pull request

## 🛠️ Development Setup

### Prerequisites
- Python 3.10 or higher
- Git
- A GitHub account

### Step-by-Step Setup

```bash
# 1. Clone your fork
git clone https://github.com/YOUR_USERNAME/email-domain-classifier.git
cd email-domain-classifier

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install in development mode with all tools
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Verify setup
pytest --version
email-cli --version
```

## 📝 Development Workflow

### Making Changes

1. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make your changes** following our coding standards.

3. **Run the development tools**:
   ```bash
   # Format code
   black .
   isort .
   
   # Type checking
   mypy email_classifier/
   
   # Run tests
   pytest
   ```

4. **Test your changes**:
   ```bash
   # Run all tests with coverage
   pytest --cov=email_classifier --cov-report=html
   
   # Test CLI functionality
   email-cli sample_emails.csv -o test_output/ --verbose
   ```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(domains): add healthcare domain classification
fix(cli): handle empty input files gracefully
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=email_classifier --cov-report=html

# Run specific test file
pytest tests/test_classifier.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Add unit tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*()`
- Use descriptive test names
- Include edge cases and error conditions
- Aim for high test coverage

Example test structure:
```python
import pytest
from email_classifier import EmailClassifier

def test_classify_finance_email():
    """Test classification of finance-related email."""
    classifier = EmailClassifier()
    result = classifier.classify_dict({
        'sender': 'security@bank.com',
        'receiver': 'user@email.com',
        'timestamp': '2024-01-15',
        'subject': 'Your account statement',
        'body': 'Dear Customer, Your monthly statement...',
        'has_url': True
    })
    assert result.domain == 'finance'
```

## 📚 Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings in Python code
2. **API Documentation**: Generated from docstrings
3. **User Documentation**: Guides and tutorials in `docs/`
4. **README**: Project overview and quick start

### Documentation Guidelines

- Write clear, concise docstrings
- Include examples in docstrings
- Keep README up to date
- Update relevant documentation when changing features
- Use proper markdown formatting

## 🔍 Code Review Process

### Before Submitting

1. **Run all tests** and ensure they pass
2. **Check code formatting** with `black --check .`
3. **Verify type checking** with `mypy email_classifier/`
4. **Update documentation** if needed
5. **Rebase** your branch if needed

### Pull Request Guidelines

1. **Use descriptive title** and PR template
2. **Link related issues** in the description
3. **Describe your changes** clearly
4. **Include screenshots** if applicable
5. **Add "ready for review"** when complete

### Review Process

- All PRs require at least one approval
- Automated checks must pass
- Reviewers may request changes
- Maintain polite, constructive communication

## 🐛 Bug Reports

### Reporting Bugs

1. **Search existing issues** first
2. **Use bug report template**
3. **Provide complete information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs
   - Sample data if relevant

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 
- OS: 
- Package version: 

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Proposing Features

1. **Check existing issues** and discussions
2. **Use feature request template**
3. **Describe the use case** and problem
4. **Propose a solution** if you have ideas
5. **Consider alternatives** and trade-offs

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this work?

## Alternatives Considered
Other approaches you thought of

## Additional Context
Any relevant information or constraints
```

## 🏗️ Architecture Guidelines

### Code Organization

- Follow existing package structure
- Single responsibility per module
- Use type hints consistently
- Write testable code
- Keep functions focused and small

### Design Patterns

- Use existing patterns in the codebase
- Follow strategy pattern for classification methods
- Use factory pattern for object creation
- Implement proper error handling

## 🤝 Community Guidelines

### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Documentation**: For usage and development guides

### Communication

- Be respectful and constructive
- Help others when you can
- Welcome newcomers and questions
- Focus on what's best for the project

## 📋 Release Process

Releases are managed by maintainers following semantic versioning:

1. **Version bump** in `pyproject.toml`
2. **Update CHANGELOG.md** with changes
3. **Create release tag** on GitHub
4. **Automated PyPI publish** via GitHub Actions

## 🎯 Priorities

Current development priorities:

1. **Bug fixes** and stability improvements
2. **New domain classifications** 
3. **Performance optimizations**
4. **Documentation improvements**
5. **Developer experience enhancements**

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributor statistics

Thank you for contributing to Email Domain Classifier! 🎉

---

If you have any questions about contributing, don't hesitate to open an issue or discussion.