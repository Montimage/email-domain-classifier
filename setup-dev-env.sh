#!/bin/bash
# setup-dev-env.sh - Automated development environment setup
# Part of Enhanced DevOps Quality Gates implementation

set -e  # Exit on any error

echo "🚀 Setting up development environment for email-domain-classifier..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install package in development mode
echo "📚 Installing package and dependencies..."
pip install -e ".[dev]"

# Install additional security and quality tools
echo "🔒 Installing security and quality tools..."
pip install detect-secrets pip-audit trufflehog xenon radon check-manifest build twine

# Install pre-commit hooks
echo "🎯 Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg

# Validate test discovery
echo "🧪 Validating test discovery..."
python -m pytest tests/ --co

# Test security tools
echo "🛡️  Testing security tools..."
detect-secrets --baseline .secrets.baseline email_classifier/ --exclude-lines ".*test.*"
pip-audit --requirement requirements.txt

# Test quality tools
echo "📊 Testing quality tools..."
xenon --max-average=A --max-modules=B --max-absolute=C email_classifier/
radon cc --min=C email_classifier/

# Create initial secrets baseline if it doesn't exist
if [ ! -f ".secrets.baseline" ]; then
    echo "🔑 Creating secrets baseline..."
    detect-secrets scan email_classifier/ > .secrets.baseline
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Run 'pre-commit run --all-files' to test all hooks"
echo "  2. Make your changes and commit normally"
echo "  3. Check 'make help' for available commands (if Makefile exists)"
echo ""
echo "🔧 All quality gates are now active and will run automatically on commits."
