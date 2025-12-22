# 📧 Email Domain Classifier

[![CI Status](https://github.com/luongnv89/email-classifier/workflows/CI/badge.svg)](https://github.com/luongnv89/email-classifier/actions)
[![codecov](https://codecov.io/gh/luongnv89/email-classifier/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/luongnv89/email-classifier)
[![PyPI version](https://badge.fury.io/py/email-classifier.svg)](https://badge.fury.io/py/email-classifier)
[![Python versions](https://img.shields.io/pypi/pyversions/email-classifier.svg)](https://pypi.org/project/email-classifier/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for classifying emails by domain using dual-method validation. Designed for processing large datasets efficiently with streaming processing and beautiful terminal output.

## ⚡ Quick Start

```bash
# Install & Run (5 minutes)
git clone git@github.com:luongnv89/email-classifier.git && cd email-classifier
python -m venv .venv && source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -e .
email-classifier sample_emails.csv -o output/
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
├── classifier.py         # Core classification logic
├── cli.py               # Command-line interface  
├── domains.py           # Domain definitions and profiles
├── processor.py         # CSV streaming processor
├── reporter.py          # Report generation
└── ui.py               # Terminal UI components

tests/                   # Test suite
spam-assasin/            # Sample data and testing tools
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

- **Dual-Method Classification**: Combines keyword taxonomy and structural analysis for accuracy
- **Streaming Processing**: Memory-efficient handling of large CSV datasets
- **Beautiful Terminal UI**: Rich progress bars, tables, and color-coded output
- **Comprehensive Reports**: JSON and text reports with detailed statistics
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Python 3.10+**: Modern Python with type hints and dataclasses

## 🤝 Contributing

We welcome contributions! Please see our [Development Playbook](docs/development-playbook.md) for:

- Development environment setup
- Code style and quality standards
- Pull request process
- Testing guidelines

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Contact

Built with ❤️ by [Montimage Security Research](https://www.montimage.com/)

- **GitHub**: [luongnv89/email-classifier](https://github.com/luongnv89/email-classifier)
- **Issues**: [Issue Tracker](https://github.com/luongnv89/email-classifier/issues)
- **Discussions**: [GitHub Discussions](https://github.com/luongnv89/email-classifier/discussions)
- **Email**: research@montimage.com

---

**Quick Links**: [Install](docs/installation.md) • [Quick Start](docs/user-guide/quick-start.md) • [API Docs](docs/api/) • [Development](docs/development-playbook.md) • [Help](docs/troubleshooting/)