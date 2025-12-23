# 📧 Email Domain Classifier

[![CI Status](https://github.com/montimage/email-domain-classifier/workflows/CI/badge.svg)](https://github.com/montimage/email-domain-classifier/actions)
[![codecov](https://codecov.io/gh/montimage/email-domain-classifier/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/montimage/email-domain-classifier)
[![PyPI version](https://badge.fury.io/py/email-domain-classifier.svg)](https://badge.fury.io/py/email-domain-classifier)
[![Python versions](https://img.shields.io/pypi/pyversions/email-domain-classifier.svg)](https://pypi.org/project/email-domain-classifier/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for classifying emails by domain using dual-method validation. Designed for processing large datasets efficiently with streaming processing and beautiful terminal output.

## ⚡ Quick Start

```bash
# Install & Run (5 minutes)
git clone git@github.com:montimage/email-domain-classifier.git && cd email-domain-classifier
python -m venv .venv && source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -e .

# Analyze your dataset first
email-cli info sample_emails.csv

# Then classify emails
email-cli sample_emails.csv -o output/
```

## 🎯 Project Overview

The Email Domain Classifier processes email datasets using sophisticated dual-method validation to accurately categorize emails into 10 business domains:

- **💰 Finance** - Banking, payments, financial services
- **💻 Technology** - Software, hardware, IT services
- **🛒 Retail** - E-commerce, shopping, consumer goods
- **📦 Logistics** - Shipping, supply chain, transportation
- **🏥 Healthcare** - Medical services, health insurance
- **🏛️ Government** - Public sector, regulatory agencies
- **👥 HR** - Human resources, recruitment, employee services
- **📞 Telecommunications** - Phone, internet, communication services
- **📱 Social Media** - Social platforms, networking services
- **🎓 Education** - Schools, universities, learning platforms

## 🏗️ Architecture

The system combines two complementary classification methods:

1. **Keyword Taxonomy Matching** - Analyzes domain-specific keywords, sender patterns, and subject patterns
2. **Structural Template Matching** - Evaluates email structure, formality, and content patterns

Emails are only classified when **both methods agree**, ensuring high-confidence classifications and reducing false positives.

## 📁 Module Structure

```
email_classifier/
├── analyzer.py          # Dataset analysis (info command)
├── classifier.py        # Core classification logic
├── cli.py               # Command-line interface
├── domains.py           # Domain definitions and profiles
├── processor.py         # CSV streaming processor
├── reporter.py          # Report generation
├── ui.py                # Terminal UI components
└── validator.py         # Email validation

tests/                   # Test suite
docs/                    # Comprehensive documentation
```

## 📚 Documentation

- **📖 [Installation Guide](docs/installation.md)** - Complete setup instructions
- **🚀 [User Guide](docs/user-guide/)** - Usage examples and tutorials
- **📡 [API Reference](docs/api/)** - Complete API documentation
- **🏛️ [Architecture](docs/architecture/)** - System design and patterns
- **🛠️ [Development](docs/development-playbook.md)** - Development setup and contribution
- **🚀 [Deployment](docs/deployment-playbook.md)** - Production deployment guide
- **🔧 [Troubleshooting](docs/troubleshooting/)** - Common issues and solutions

## 🔬 Key Features

- **Dataset Analysis**: `info` command to analyze datasets before classification (label distribution, body lengths, sender domains, data quality)
- **Dual-Method Classification**: Combines keyword taxonomy and structural analysis for accuracy
- **Streaming Processing**: Memory-efficient handling of large CSV datasets
- **Data Validation**: Validates email records (valid sender/receiver format, non-empty subject/body) before processing
- **Standardized Output**: Consistent column structure: `sender, receiver, date, subject, body, urls, label`
- **Beautiful Terminal UI**: Rich progress bars, tables, charts, and color-coded output
- **Comprehensive Reports**: JSON and text reports with detailed statistics
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Python 3.10+**: Modern Python with type hints and dataclasses

## 📊 Dataset Analysis

Before classifying, analyze your dataset to understand its structure:

```bash
# Terminal report with charts
email-cli info emails.csv

# Machine-readable JSON output
email-cli info emails.csv --json
```

The info command displays:
- **Label distribution** - Bar chart of existing labels
- **Body length histogram** - Distribution of email lengths
- **Top sender domains** - Most common sender domains
- **Data quality** - Missing fields, invalid formats, URL presence

## 📊 Data Validation

The classifier validates each email before processing:

- **Email Format**: Validates sender and receiver have valid email format
- **Required Fields**: Ensures subject and body are not empty/whitespace-only
- **Invalid Email Handling**: Invalid emails are logged to `invalid_emails.csv` with error reasons

Use `--strict-validation` to fail processing on first invalid email (default: skip and log).

## 📋 Output Structure

All output CSV files have a standardized column structure:

| Column | Description |
|--------|-------------|
| `sender` | Email sender address |
| `receiver` | Email recipient address |
| `date` | Date/timestamp (mapped from `timestamp` if needed) |
| `subject` | Email subject line |
| `body` | Email body content |
| `urls` | URL presence (mapped from `has_url` if needed) |
| `label` | Classified domain |
| `classified_domain` | Classified domain (same as label) |
| `method1_domain` | Domain from keyword method |
| `method2_domain` | Domain from structural method |

## 🤝 Contributing

We welcome contributions! Please see our [Development Playbook](docs/development-playbook.md) for:

- Development environment setup
- Code style and quality standards
- Pull request process
- Testing guidelines

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 📞 Contact

Built with ❤️ by [Montimage Security Research](https://www.montimage.com/)

- **GitHub**: [montimage/email-domain-classifier](https://github.com/montimage/email-domain-classifier)
- **Issues**: [Issue Tracker](https://github.com/montimage/email-domain-classifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/montimage/email-domain-classifier/discussions)
- **Email**: research@montimage.com

---

**Quick Links**: [Install](docs/installation.md) • [Quick Start](docs/user-guide/quick-start.md) • [API Docs](docs/api/) • [Development](docs/development-playbook.md) • [Help](docs/troubleshooting/)
