# Email Domain Classifier Documentation

Welcome to the Email Domain Classifier documentation! This powerful Python library classifies emails by domain using dual-method validation combining keyword taxonomy matching and structural template analysis.

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
user-guide/index
api/index
developer-guide/index
contributing
changelog
```

## 🚀 Quick Start

```bash
# Install and run in 5 minutes
git clone https://github.com/luongnv89/email-classifier.git
cd email-classifier
python -m venv .venv && source .venv/bin/activate
pip install -e .
email-classifier sample_emails.csv -o output/
```

## ✨ Key Features

- **Dual-Method Classification**: Combines keyword taxonomy and structural template analysis for accurate domain classification
- **Streaming Processing**: Memory-efficient processing of large CSV datasets  
- **Beautiful Terminal UI**: Rich progress bars, tables, and color-coded output
- **10 Domain Categories**: Finance, Technology, Retail, Logistics, Healthcare, Government, HR, Telecommunications, Social Media, Education
- **Comprehensive Reports**: JSON and text reports with statistics and recommendations

## 📋 Supported Domains

| Domain | Icon | Description |
|---------|-------|-------------|
| 💰 Finance | Banking, payments, financial services |
| 💻 Technology | Software, hardware, IT services |
| 🛒 Retail | E-commerce, shopping, consumer goods |
| 📦 Logistics | Shipping, supply chain, transportation |
| 🏥 Healthcare | Medical services, health insurance |
| 🏛️ Government | Public sector, regulatory agencies |
| 👥 HR | Human resources, recruitment, employee services |
| 📞 Telecommunications | Phone, internet, communication services |
| 📱 Social Media | Social platforms, networking services |
| 🎓 Education | Schools, universities, learning platforms |

## 🔗 Links

- **GitHub Repository**: https://github.com/luongnv89/email-classifier
- **PyPI Package**: https://pypi.org/project/email-classifier/
- **Issue Tracker**: https://github.com/luongnv89/email-classifier/issues
- **Discussions**: https://github.com/luongnv89/email-classifier/discussions

## 📚 Table of Contents

### User Documentation
- [Installation Guide](installation) - How to install and set up the classifier
- [User Guide](user-guide/index) - Complete usage guide with examples
- [Examples & Recipes](user-guide/examples) - Practical examples for common scenarios

### API Documentation  
- [API Reference](api/index) - Complete API documentation
- [EmailClassifier Class](api/email_classifier) - Main classification interface
- [StreamingProcessor](api/processor) - Batch processing utilities
- [CLI Interface](api/cli) - Command-line interface

### Developer Documentation
- [Developer Guide](developer-guide/index) - Development setup and contribution guide
- [Architecture](developer-guide/architecture) - Project architecture and design patterns
- [Adding New Domains](developer-guide/extending) - How to add custom domain classifications
- [Testing](developer-guide/testing) - Testing guidelines and best practices

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing) for details on:

- How to set up development environment
- Code style and quality standards  
- Submitting pull requests
- Reporting bugs and requesting features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/luongnv89/email-classifier/blob/main/LICENSE) file for details.

## 🆘 Getting Help

- **Documentation**: Read through this site for comprehensive guidance
- **GitHub Issues**: [Search existing issues](https://github.com/luongnv89/email-classifier/issues) or [create a new one](https://github.com/luongnv89/email-classifier/issues/new)
- **GitHub Discussions**: [Ask questions](https://github.com/luongnv89/email-classifier/discussions) and share ideas
- **Email**: Contact us at research@montimage.com

---

Built with ❤️ by Montimage Security Research