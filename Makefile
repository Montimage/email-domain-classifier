# Makefile for email-classifier development operations
# Part of Enhanced DevOps Quality Gates implementation

.PHONY: help install install-dev setup lint security quality test clean all

# Default target
help: ## Show this help message
	@echo "🎯 Email Classifier Development Commands:"
	@echo ""
	@echo "🔧 Setup & Installation:"
	@echo "  install       Install package in development mode"
	@echo "  install-dev   Install package with dev dependencies"
	@echo "  setup         Run complete development environment setup"
	@echo ""
	@echo "🔍 Quality & Security:"
	@echo "  lint          Run all linting tools"
	@echo "  security      Run security scans"
	@echo "  quality       Run code quality checks"
	@echo "  test          Run test suite"
	@echo "  all           Run all quality checks"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean         Clean build artifacts"
	@echo "  pre-commit    Run pre-commit hooks on all files"

install: ## Install package in development mode
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev]"

setup: ## Run complete development environment setup
	./setup-dev-env.sh

lint: ## Run all linting tools (black, isort, flake8, mypy, pydocstyle)
	@echo "🔍 Running linting tools..."
	black --check --diff .
	isort --check-only --diff .
	mypy email_classifier/
	flake8 email_classifier/
	pydocstyle --convention=google email_classifier/

security: ## Run security scans (detect-secrets, pip-audit, trufflehog)
	@echo "🛡️  Running security scans..."
	detect-secrets scan --baseline .secrets.baseline email_classifier/
	pip-audit --requirement requirements.txt
	# Note: trufflehog requires git URL, so we skip it in local checks
	@echo "ℹ️  Note: trufflehog will run in CI pipeline for full git history scanning"

quality: ## Run code quality checks (xenon, radon)
	@echo "📊 Running quality checks..."
	xenon --max-average=A --max-modules=B --max-absolute=C .
	radon cc --min=C email_classifier/

test: ## Run test suite with coverage
	@echo "🧪 Running test suite..."
	pytest --cov=email_classifier --cov-report=term-missing --cov-report=html --cov-report=xml

all: ## Run all quality checks (lint, security, quality, test)
	@echo "🎯 Running all quality checks..."
	$(MAKE) lint
	$(MAKE) security
	$(MAKE) quality
	$(MAKE) test

clean: ## Clean build artifacts and cache files
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

pre-commit: ## Run pre-commit hooks on all files
	@echo "🎯 Running pre-commit hooks on all files..."
	pre-commit run --all-files

# Development shortcuts
dev: install-dev ## Alias for install-dev

check: all ## Alias for all quality checks