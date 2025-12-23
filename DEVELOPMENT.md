# Developer Onboarding Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git for version control
- Make (optional, but recommended)

### Initial Setup

#### 1. Clone Repository
```bash
git clone https://github.com/montimage/email-domain-classifier.git
cd email-domain-classifier
```

#### 2. Automated Setup (Recommended)
```bash
# One-command setup - installs dependencies, tools, and configures everything
./setup-dev-env.sh
```

#### 3. Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Create initial secrets baseline
detect-secrets scan email_classifier/ > .secrets.baseline
```

## 🛠️ Development Workflow

### Quality Gates

The project uses comprehensive quality gates that run automatically:

#### Pre-commit Hooks (Local)
- **Security**: detect-secrets, pip-audit, trufflehog
- **Linting**: black, isort, flake8, mypy, pydocstyle
- **Quality**: xenon (complexity), radon (metrics)
- **Build**: pyproject-build, twine-check, check-manifest
- **Testing**: pytest with coverage

#### GitHub Actions (CI/CD)
- **Security Comprehensive**: Secret scanning, SBOM generation, container security
- **Quality Gates**: Coverage enforcement, complexity analysis, performance testing
- **Build Verification**: Multi-platform testing, artifact integrity verification

### Development Commands

```bash
# Setup your environment
make setup

# Run all quality checks locally
make all

# Individual checks
make lint       # Code formatting and linting
make security   # Security scanning
make quality    # Code quality analysis
make test       # Test suite
make clean      # Clean build artifacts

# Run pre-commit hooks manually
make pre-commit
```

## 📊 Quality Standards

### Code Complexity
- **Average**: ≤ 7.0 (Grade A)
- **Module**: ≤ 10.0 (Grade B)
- **Absolute**: ≤ 15.0 (Grade C)

### Code Coverage
- **Overall**: ≥ 90%
- **File**: ≥ 80%
- **Critical modules**: ≥ 95%

### Performance
- **Hook execution**: < 30 seconds
- **CI pipeline**: < 10 minutes

## 🔒 Security Guidelines

### Secret Management
- Never commit secrets to the repository
- Use environment variables for sensitive data
- Test secret detection with baseline: `detect-secrets scan --baseline .secrets.baseline`

### Dependency Security
- Regular updates: Run `make security` to check for vulnerabilities
- Review security reports in GitHub Actions artifacts

## 🐛 Troubleshooting

### Common Issues

#### Pre-commit Hook Failures
```bash
# Hook not found?
pre-commit install

# Hook failed?
pre-commit run --all-files  # Run on all files to debug

# Specific tool failing?
make lint      # Or make security, make quality
```

#### Virtual Environment Issues
```bash
# Python version mismatch?
python --version
# Should be 3.10+

# Module not found?
pip install -e ".[dev]"  # Reinstall with dev dependencies
```

#### Performance Issues
```bash
# Slow pre-commit hooks?
make clean  # Clear caches
rm -rf .pre-commit  # Clear pre-commit cache

# Slow CI?
# Check GitHub Actions logs for bottlenecks
# Consider reducing test scope or optimizing caching
```

## 📚 Development Resources

### Documentation
- [README.md](README.md) - Main project documentation
- [pyproject.toml](pyproject.toml) - Project configuration
- [AGENTS.md](AGENTS.md) - Development guidelines

### Code Structure
```
email_classifier/
├── __init__.py          # Package initialization
├── classifier.py         # Core classification logic
├── domains.py            # Domain definitions and profiles
├── processor.py          # Data processing and streaming
├── reporter.py           # Report generation and statistics
├── ui.py                 # Terminal user interface
└── cli.py                 # Command-line interface

tests/                      # Test suite
├── test_classifier.py
├── test_domains.py
└── test_enhanced_statistics.py

.github/workflows/           # CI/CD pipelines
├── ci.yml               # Continuous integration
├── docs.yml             # Documentation building
├── release.yml           # Release automation
├── security-comprehensive.yml  # Security scanning
├── quality-gates.yml    # Quality enforcement
└── build-verification.yml  # Build verification
```

## 🤝 Contributing

### Commit Messages
Follow conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes

### Pull Request Process
1. Fork and create feature branch
2. Make changes with quality gates active
3. Ensure all checks pass locally: `make all`
4. Submit PR with clear description
5. Address any CI failures promptly

## 📞 Getting Help

### Support Channels
- **GitHub Issues**: Create new issue for bugs/features
- **Documentation**: Check existing issues and docs first
- **Discussions**: Use GitHub Discussions for questions

### Quick Commands Reference
```bash
# Development workflow
./setup-dev-env.sh && make all

# Testing and quality
pytest tests/                 # Run tests
make lint                    # Run linting
make security                 # Run security checks
make quality                  # Run quality analysis
make all                     # Run everything

# Package building
python -m build              # Build package
twine check dist/*           # Check package integrity
```

---

Welcome to the team! 🎉 This setup ensures high-quality, secure, and maintainable code contributions.