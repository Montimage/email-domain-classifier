# 📧 Email Domain Classifier

A Python library for classifying emails by domain using dual-method validation. Designed for processing large datasets efficiently with streaming processing and beautiful terminal output.

## ⚡ Quick Reference

```bash
# Install & Run (5 minutes)
git clone git@github.com:luongnv89/email-classifier.git && cd email-classifier
python -m venv .venv && source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -e .
email-classifier sample_emails.csv -o output/
```

## ✨ Features

- **Dual-Method Classification**: Combines keyword taxonomy matching and structural template analysis for accurate domain classification
- **Streaming Processing**: Memory-efficient processing of large CSV datasets
- **Beautiful Terminal UI**: Rich progress bars, tables, and color-coded output
- **Comprehensive Logging**: Detailed logs for debugging and auditing
- **Detailed Reports**: JSON and text reports with statistics and recommendations
- **10 Domain Categories**: Finance, Technology, Retail, Logistics, Healthcare, Government, HR, Telecommunications, Social Media, Education

## 🚀 Quick Start

### Prerequisites

- **Python 3.10 or higher** - Check with `python --version`
- **pip** - Package installer (comes with Python)
- **git** - Version control (for cloning the repository)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
# Clone the repository
git clone git@github.com:luongnv89/email-classifier.git

# Navigate into the project directory
cd email-classifier
```

#### 2. Set Up Virtual Environment (Recommended)
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

#### 3. Install the Package
```bash
# Install in development mode (includes all dependencies)
pip install -e .

# OR for development with extra tools:
pip install -e ".[dev]"
```

#### 4. Verify Installation
```bash
# Check that the CLI is available
email-classifier --version

# List supported domains
email-classifier --list-domains

# Test Python import
python -c "from email_classifier import EmailClassifier; print('✅ Import successful')"
```

### Alternative Installation Methods

#### From PyPI (when published)
```bash
# Install from PyPI
pip install email-classifier

# Or install with development tools
pip install email-classifier[dev]
```

#### Install from Source (Direct)
```bash
# Download and install without git
curl -L https://github.com/luongnv89/email-classifier/archive/main.zip -o email-classifier.zip
unzip email-classifier.zip
cd email-classifier-main
pip install -e .
```

### Basic Usage

#### 1. Prepare Your Data
Create or obtain a CSV file with email data. **Use the provided sample data** to get started:
```bash
# Copy sample data for testing
cp sample_emails.csv test_emails.csv
```

#### 2. Run Classification
```bash
# Basic classification
email-classifier sample_emails.csv -o classified_emails/

# With verbose output (shows progress and details)
email-classifier sample_emails.csv -o classified_emails/ --verbose

# Include detailed classification scores in output files
email-classifier sample_emails.csv -o classified_emails/ --include-details

# Process large files with custom chunk size
email-classifier large_dataset.csv -o results/ --chunk-size 500

# Quiet mode (suppress console output except errors)
email-classifier data.csv -o output/ --quiet
```

#### 3. Check Results
```bash
# List output files
ls -la classified_emails/

# View classification report
cat classified_emails/classification_report.txt

# Check processing log
tail -f classified_emails/classification.log
```

## 📋 Input Format

The input CSV file should contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `sender` | Email sender address | `security@bank.com` |
| `receiver` | Email recipient address | `user@company.com` |
| `timestamp` | Email timestamp | `2024-01-15 10:30:00` |
| `subject` | Email subject line | `Your account statement is ready` |
| `body` | Email body content | `Dear Customer, Your monthly statement...` |
| `has_url` | Whether email contains URLs | `true` / `false` / `1` / `0` |

## 📂 Output Files

The classifier generates:

```
output/
├── email_finance.csv          # Emails classified as finance
├── email_technology.csv       # Emails classified as technology
├── email_retail.csv           # Emails classified as retail
├── email_logistics.csv        # Emails classified as logistics
├── email_healthcare.csv       # Emails classified as healthcare
├── email_government.csv       # Emails classified as government
├── email_hr.csv               # Emails classified as HR
├── email_telecommunications.csv
├── email_social_media.csv
├── email_education.csv
├── email_unsure.csv           # Unclassified emails
├── classification.log         # Detailed processing log
├── classification_report.json # Machine-readable report
└── classification_report.txt  # Human-readable report
```

## 🔧 Classification Methods

### Method 1: Keyword Taxonomy Matching

Scores emails based on:
- **Primary Keywords**: Domain-specific terms (weighted heavily)
- **Secondary Keywords**: Supporting terminology
- **Sender Patterns**: Email domain patterns
- **Subject Patterns**: Subject line patterns

### Method 2: Structural Template Matching

Analyzes email structure:
- Body length and paragraph count
- Presence of greeting/signature/disclaimer
- Formality level (formal, semi-formal, casual)
- URL expectation matching
- Sender structure analysis

### Classification Logic

An email is assigned to a domain only when **both methods agree**. Otherwise, it's marked as `unsure`. This dual validation reduces false positives and ensures high-confidence classifications.

## 🖥️ CLI Options

```
email-classifier [OPTIONS] INPUT

Arguments:
  INPUT                     Path to input CSV file

Options:
  -o, --output DIR          Output directory (required)
  --chunk-size INT          Processing chunk size (default: 1000)
  --include-details         Include classification scores in output
  -v, --verbose             Verbose console output
  -q, --quiet               Suppress console output
  --log-file PATH           Custom log file path
  --no-report               Skip report generation
  --json-only               Generate only JSON report
  --list-domains            List supported domains and exit
  --version                 Show version
  --help                    Show help message
```

## 🔧 Troubleshooting

### Common Installation Issues

#### "Python not found" or Version Issues
```bash
# Check Python version
python --version
python3 --version

# On macOS, install Python 3.10+:
brew install python@3.11

# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv

# On Windows: Download from python.org
```

#### "pip command not found"
```bash
# Ensure pip is installed and up to date
python -m pip install --upgrade pip

# Use python -m pip if pip is not in PATH
python -m pip install -e .
```

#### "Permission denied" during installation
```bash
# Use user directory installation
pip install --user -e .

# Or fix permissions (Unix/Linux)
sudo chown -R $USER:.local
```

#### Import errors after installation
```bash
# Reinstall in development mode
pip uninstall email-classifier
pip install -e .

# Verify package location
pip show email-classifier
```

### Common Runtime Issues

#### "No such file or directory" for input CSV
```bash
# Check file exists and is readable
ls -la your_data.csv

# Use absolute path if needed
email-classifier /full/path/to/data.csv -o output/
```

#### "CSV format error"
- Ensure your CSV has the required columns: `sender`, `receiver`, `timestamp`, `subject`, `body`, `has_url`
- Check for special characters or encoding issues
- Try converting to UTF-8 encoding

#### Memory issues with large files
```bash
# Reduce chunk size for memory efficiency
email-classifier huge_file.csv -o output/ --chunk-size 100

# Monitor memory usage
email-classifier data.csv -o output/ --verbose
```

#### Empty or unexpected results
```bash
# Enable verbose output to debug
email-classifier data.csv -o output/ --verbose --include-details

# Check the classification log
cat output/classification.log

# Verify domain categories
email-classifier --list-domains
```

### Getting Help

If you encounter issues:
1. **Check the log file** for detailed error messages
2. **Run with `--verbose`** to see processing details
3. **Verify input format** matches the required columns
4. **Check this troubleshooting section** for common solutions
5. **Open an issue** on GitHub with:
   - Your input file format (first few rows)
   - Command used
   - Error messages from the log file
   - Your operating system and Python version

## 📊 Example Report Output

```
═══════════════════════════════════════════════════════════════════════════════
                    EMAIL CLASSIFICATION REPORT
═══════════════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────────────
  SUMMARY
──────────────────────────────────────────────────────────────────────────────
  Total Emails Processed:  10,000
  Successfully Classified: 7,542 (75.42%)
  Unsure/Unclassified:     2,458
  Errors:                  0 (0.00%)
  Unique Domains Found:    8

──────────────────────────────────────────────────────────────────────────────
  DOMAIN BREAKDOWN
──────────────────────────────────────────────────────────────────────────────
  💰 Finance              ██████████████████████████████    2,341 ( 23.4%)
  💻 Technology           ████████████████████░░░░░░░░░░    1,876 ( 18.8%)
  🛒 Retail               ████████████████░░░░░░░░░░░░░░    1,523 ( 15.2%)
  📦 Logistics            ████████████░░░░░░░░░░░░░░░░░░      987 (  9.9%)
  ...
```

## 🐍 Python API

```python
from email_classifier import EmailClassifier, StreamingProcessor

# Simple classification
classifier = EmailClassifier()
domain, details = classifier.classify_dict({
    'sender': 'noreply@bank.com',
    'receiver': 'user@email.com',
    'timestamp': '2024-01-15',
    'subject': 'Your account statement',
    'body': 'Dear Customer, Your monthly statement is ready...',
    'has_url': True
})

print(f"Domain: {domain}")
print(f"Method 1: {details['method1']['domain']}")
print(f"Method 2: {details['method2']['domain']}")
print(f"Agreement: {details['agreement']}")

# Batch processing
processor = StreamingProcessor(classifier=classifier)
stats = processor.process(
    input_path='emails.csv',
    output_dir='output/',
    include_details=True
)

print(f"Processed: {stats.total_processed}")
print(f"Classified: {stats.total_classified}")
```

## 🏗️ Architecture

```
email_classifier/
├── __init__.py          # Package exports
├── classifier.py        # Classification methods
├── domains.py           # Domain definitions & taxonomies
├── processor.py         # Streaming CSV processor
├── reporter.py          # Report generation
├── ui.py                # Terminal UI components
└── cli.py               # CLI application
```

## 🔬 Extending Domains

Add custom domains by modifying `domains.py`:

```python
from email_classifier.domains import DOMAINS, DomainProfile

DOMAINS["custom_domain"] = DomainProfile(
    name="custom_domain",
    display_name="🏢 Custom",
    color="bright_green",
    primary_keywords={"keyword1", "keyword2"},
    secondary_keywords={"support1", "support2"},
    sender_patterns=[r".*@custom\.com"],
    subject_patterns=[r".*custom.*"],
    typical_body_length=(100, 2000),
    has_greeting=True,
    has_signature=True,
    has_disclaimer=False,
    url_expected=True,
    formality_level="formal",
    typical_paragraph_count=(2, 5)
)
```

## 📝 License

MIT License - See LICENSE file for details.

## 🛠️ Development Setup

For developers who want to contribute to the project:

### Setting Up Development Environment
```bash
# 1. Clone and navigate to project
git clone git@github.com:luongnv89/email-classifier.git
cd email-classifier

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install in development mode with dev tools
pip install -e ".[dev]"
```

### Development Workflow
```bash
# 1. Run code formatting
black email_classifier/ tests/
isort email_classifier/ tests/

# 2. Type checking
mypy email_classifier/

# 3. Run tests
pytest

# 4. Run tests with coverage
pytest --cov=email_classifier --cov-report=html

# 5. Test CLI functionality
email-classifier sample_emails.csv -o test_output/ --verbose
```

### Project Structure
```
email-classifier/
├── email_classifier/          # Main package
│   ├── __init__.py          # Package exports and version
│   ├── classifier.py         # Core classification logic
│   ├── cli.py               # Command-line interface
│   ├── domains.py            # Domain definitions and profiles
│   ├── processor.py          # CSV streaming processor
│   ├── reporter.py           # Report generation
│   └── ui.py                # Terminal UI components
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_classifier.py    # Classification tests
│   └── test_domains.py      # Domain definition tests
├── pyproject.toml           # Modern Python packaging config
├── setup.py                 # Legacy setup configuration
├── requirements.txt         # Runtime dependencies
├── sample_emails.csv        # Sample data for testing
└── README.md               # This file
```

### Code Style and Standards
- **Python 3.10+** compatibility
- **PEP 8** compliance with Black formatting
- **Type hints** using standard typing module
- **Docstrings** following Google/NumPy style
- **Line length**: 88 characters (Black default)

## 🤝 Contributing

Contributions welcome! Please follow these steps:

### How to Contribute
1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following development standards
4. **Run tests**: `pytest` and ensure they pass
5. **Format code**: `black .` and `isort .`
6. **Type check**: `mypy email_classifier/`
7. **Commit changes**: `git commit -m 'Add amazing feature'`
8. **Push to fork**: `git push origin feature/amazing-feature`
9. **Open a Pull Request** with detailed description

### Contribution Guidelines
- **Bug fixes**: Include tests that reproduce the bug
- **New features**: Include tests and update documentation
- **Breaking changes**: Clearly document in PR description
- **Documentation**: Keep README and docstrings current
- **Code style**: Run formatters before committing

### Reporting Issues
When reporting bugs, please include:
- **Python version**: `python --version`
- **Operating system**: `uname -a` (Linux/macOS) or system info
- **Input data**: Sample of problematic email data
- **Error messages**: Full traceback and log output
- **Steps to reproduce**: Clear reproduction steps

### Feature Requests
- **Use cases**: Describe what problem this solves
- **Proposed solution**: How you envision the feature
- **Alternatives**: Other approaches you considered
- **Additional context**: Any relevant domain knowledge

## ✅ Verification Checklist

After installation, verify your setup:

### Installation Verification
- [ ] `email-classifier --version` shows version information
- [ ] `email-classifier --list-domains` shows 10 domains
- [ ] `from email_classifier import EmailClassifier` works in Python
- [ ] `pip show email-classifier` shows package details

### Basic Functionality Test
- [ ] `email-classifier sample_emails.csv -o test_output/` runs without errors
- [ ] Output directory contains `email_*.csv` files
- [ ] `classification_report.txt` shows processing statistics
- [ ] Log file `classification.log` contains processing details

### Development Setup (for contributors)
- [ ] `pytest` runs successfully
- [ ] `black --check .` passes formatting check
- [ ] `mypy email_classifier/` completes without errors
- [ ] `email-classifier --help` shows all options

---

Built with ❤️ by Montimage Security Research
