# Email Classifier Module

Core module for the Email Domain Classifier package. This module contains the main classification logic, domain definitions, and data processing components.

## 🏗️ Module Structure

```
email_classifier/
├── __init__.py          # Package exports and version
├── classifier.py         # Core classification logic
├── cli.py               # Command-line interface
├── domains.py           # Domain definitions and profiles
├── processor.py         # CSV streaming processor
├── reporter.py          # Report generation
├── ui.py               # Terminal UI components
└── py.typed           # Type hints marker
```

## 🔧 Installation & Setup

### For Development

If you're working on this module specifically:

```bash
# Clone repository
git clone https://github.com/luongnv89/email-classifier.git
cd email-classifier

# Set up development environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all module tests
pytest tests/

# Run specific module tests
pytest tests/test_classifier.py
pytest tests/test_domains.py

# Run with coverage
pytest --cov=email_classifier --cov-report=html
```

### Code Quality

```bash
# Format code
black email_classifier/
isort email_classifier/

# Type checking
mypy email_classifier/

# Run pre-commit hooks
pre-commit run --all-files
```

## 📋 Key Components

### EmailClassifier (`classifier.py`)

Main classification engine using dual-method validation:

```python
from email_classifier import EmailClassifier

classifier = EmailClassifier()
domain, details = classifier.classify_dict({
    'sender': 'noreply@bank.com',
    'receiver': 'user@email.com',
    'subject': 'Your account statement',
    'body': 'Dear Customer...',
    'has_url': True
})
```

### DomainProfiles (`domains.py`)

Defines the 10 business domain categories with their characteristics:

```python
from email_classifier.domains import DOMAINS

# Access domain definitions
finance_profile = DOMAINS['finance']
print(finance_profile.primary_keywords)
```

### StreamingProcessor (`processor.py`)

Handles large datasets efficiently with streaming processing:

```python
from email_classifier import StreamingProcessor

processor = StreamingProcessor()
stats = processor.process('emails.csv', 'output/')
```

### ReportGenerator (`reporter.py`)

Creates comprehensive classification reports:

```python
from email_classifier.reporter import ReportGenerator

generator = ReportGenerator()
report = generator.generate_text_report(classification_stats)
```

### TerminalUI (`ui.py`)

Provides beautiful terminal output and progress tracking:

```python
from email_classifier.ui import TerminalUI

ui = TerminalUI()
ui.print_progress(current, total, "Processing emails...")
```

## 🧪 Testing

### Test Data

The module includes test data in `sample_emails.csv` for consistent testing:

```bash
# Use sample data for quick testing
email-classifier sample_emails.csv -o test_output/
```

### Test Categories

- **Unit Tests** (`test_classifier.py`) - Classification method testing
- **Domain Tests** (`test_domains.py`) - Domain profile validation
- **Integration Tests** (`test_enhanced_statistics.py`) - End-to-end workflow testing

### Running Individual Tests

```bash
# Test specific classification scenarios
pytest tests/test_classifier.py::test_dual_method_agreement

# Test domain profiles
pytest tests/test_domains.py::test_domain_completeness

# Test with verbose output
pytest -v tests/test_classifier.py
```

## 🔍 Debugging

### Enable Debug Mode

```bash
# Run with verbose logging
email-classifier data.csv -o output/ --verbose

# Include detailed classification scores
email-classifier data.csv -o output/ --include-details

# Custom log file
email-classifier data.csv -o output/ --log-file debug.log
```

### Python Debugging

```python
import logging
from email_classifier import EmailClassifier

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Test classification with details
classifier = EmailClassifier()
result = classifier.classify_dict(email_data, include_details=True)
print(f"Classification result: {result}")
```

## 📊 Module Dependencies

### Required Dependencies

- **rich** - Terminal UI components and formatting

### Optional Dependencies (Development)

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **isort** - Import sorting
- **mypy** - Type checking

## 🚀 Extending the Module

### Adding New Domains

1. Define domain profile in `domains.py`:

```python
DOMAINS["new_domain"] = DomainProfile(
    name="new_domain",
    display_name="🆕 New Domain",
    color="bright_green",
    primary_keywords={"keyword1", "keyword2"},
    secondary_keywords={"support1", "support2"},
    # ... other properties
)
```

2. Update classification logic if needed
3. Add tests for the new domain
4. Update documentation

### Adding New Classification Methods

1. Implement method in `classifier.py`
2. Integrate with dual-method validation
3. Add comprehensive tests
4. Update documentation and examples

## 🔧 Module Configuration

### Environment Variables

```bash
# Set default log level
export EMAIL_CLASSIFIER_LOG_LEVEL=INFO

# Set default chunk size
export EMAIL_CLASSIFIER_CHUNK_SIZE=1000

# Disable progress bars
export EMAIL_CLASSIFIER_QUIET=true
```

### Configuration Files

The module respects configuration in this order:

1. Environment variables
2. Command-line arguments
3. Default values

## 📞 Support

For module-specific issues:

1. **Check module tests**: `pytest tests/`
2. **Review documentation**: [API Docs](../api/)
3. **Search existing issues**: [GitHub Issues](https://github.com/luongnv89/email-classifier/issues)
4. **Create new issue**: Include module name in issue title

## 📝 Contributing

When contributing to this module:

1. **Follow code style**: `black . && isort .`
2. **Add tests**: All new features need tests
3. **Type checking**: `mypy email_classifier/`
4. **Update documentation**: Keep docs in sync
5. **Run pre-commit**: `pre-commit run --all-files`

---

**Related Documentation**:
- [API Reference](../api/) - Detailed API documentation
- [User Guide](../user-guide/) - Usage examples
- [Architecture](../architecture/) - System design
- [Development Guide](../development-playbook.md) - Development setup