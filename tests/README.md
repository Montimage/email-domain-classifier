# Tests Module

Comprehensive test suite for Email Domain Classifier. This module contains unit tests, integration tests, and quality assurance procedures.

## 🏗️ Test Structure

```
tests/
├── __init__.py                    # Test package marker
├── test_classifier.py             # Core classification tests
├── test_domains.py               # Domain profile tests
├── test_enhanced_statistics.py   # Integration and statistics tests
└── fixtures/                    # Test data and fixtures (if needed)
```

## 🚀 Running Tests

### Quick Test Run

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=email_classifier --cov-report=html
```

### Test Categories

#### Classification Tests (`test_classifier.py`)

Tests core classification functionality:

```bash
# Run classification tests
pytest tests/test_classifier.py -v

# Run specific test methods
pytest tests/test_classifier.py::test_classify_dict -v
pytest tests/test_classifier.py::test_dual_method_agreement -v
```

**Key test scenarios:**
- Single email classification
- Dual-method validation
- Edge cases and error handling
- Performance and memory usage

#### Domain Tests (`test_domains.py`)

Tests domain profiles and taxonomy:

```bash
# Run domain tests
pytest tests/test_domains.py -v

# Test specific domains
pytest tests/test_domains.py::test_finance_domain -v
pytest tests/test_domains.py::test_all_domains_coverage -v
```

**Key test scenarios:**
- Domain profile completeness
- Keyword accuracy
- Pattern matching
- Cross-domain interference

#### Integration Tests (`test_enhanced_statistics.py`)

Tests end-to-end workflows:

```bash
# Run integration tests
pytest tests/test_enhanced_statistics.py -v

# Test statistics generation
pytest tests/test_enhanced_statistics.py::test_statistics_accuracy -v
```

## 🔧 Test Configuration

### Environment Setup

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install test dependencies
pip install -e ".[dev]"

# Verify test setup
pytest --version
```

### Test Configuration File

Create `pytest.ini` or `pyproject.toml` configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]
```

## 📊 Test Coverage

### Coverage Requirements

- **Overall coverage**: ≥ 90%
- **Core modules**: ≥ 95%
- **Classification logic**: 100%

### Running Coverage

```bash
# Generate coverage report
pytest --cov=email_classifier --cov-report=html --cov-report=term

# Open HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows

# Generate coverage badge
coverage-badge
```

### Coverage Exclusions

Certain areas are excluded from coverage:

```python
# test_classifier.py
# Type checking and validation
if not isinstance(email, dict):
    return "unsure", {"error": "Invalid input type"}

# Performance optimization
if len(keywords) > 1000:  # pragma: no cover
    # Edge case handling
```

## 🧪 Test Data

### Using Sample Data

The project includes `sample_emails.csv` for testing:

```bash
# Test with provided sample data
pytest tests/test_classifier.py::test_with_sample_data -v

# Copy sample data for custom tests
cp sample_emails.csv tests/fixtures/test_data.csv
```

### Test Data Requirements

Test data should include:

- **All 10 domains** with representative examples
- **Edge cases** (empty fields, special characters)
- **Unclassified emails** for negative testing
- **Large datasets** for performance testing

### Generating Test Data

```bash
# Generate synthetic test data
python -m email_classifier.cli --generate-test-data \
  --output tests/fixtures/generated_data.csv \
  --count 1000 \
  --domains all
```

## 🔍 Debugging Tests

### Verbose Test Output

```bash
# Maximum verbosity
pytest -v -s --tb=long

# Show print statements
pytest -s tests/test_classifier.py::test_specific_case

# Debug with pdb
pytest --pdb tests/test_classifier.py::test_failing_case
```

### Test Logging

```bash
# Enable debug logging in tests
pytest --log-cli-level=DEBUG tests/test_classifier.py

# Capture log output
pytest --log-cli-level=DEBUG --capture=no tests/
```

### Isolating Test Failures

```bash
# Run only failing tests
pytest --lf  # last-failed

# Run tests until first failure
pytest -x

# Run specific test file
pytest tests/test_classifier.py::test_failing_function -v
```

## 📈 Performance Testing

### Benchmark Tests

```bash
# Run performance benchmarks
pytest tests/test_classifier.py::test_classification_performance -v

# Memory usage testing
pytest tests/test_processor.py::test_large_dataset_memory -v
```

### Performance Criteria

- **Single email classification**: < 10ms
- **1000 email batch**: < 2 seconds
- **Memory usage**: < 100MB for 10K emails
- **Large file processing**: No memory leaks

## 🔧 Test Maintenance

### Adding New Tests

1. **Follow naming conventions**:
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test functions: `test_*`

2. **Use proper assertions**:
   ```python
   # Good practices
   assert result == expected
   assert isinstance(domain, str)
   assert "finance" in domain
   
   # With descriptive messages
   assert domain == "finance", f"Expected 'finance', got '{domain}'"
   ```

3. **Include edge cases**:
   ```python
   # Test boundary conditions
   def test_empty_email(self):
       result = classifier.classify_dict({})
       assert result[0] == "unsure"
   
   def test_malformed_data(self):
       with pytest.raises(ValueError):
           classifier.classify_dict(None)
   ```

### Test Documentation

Each test should have:

- **Clear purpose** in docstring
- **Descriptive name** explaining what's tested
- **Setup and teardown** if needed
- **Assertions** with meaningful messages

```python
def test_classify_finance_email_with_keywords(self):
    """Test that finance-related keywords result in finance classification."""
    # Arrange
    email_data = {
        "sender": "bank@financial.com",
        "subject": "Account Statement",
        "body": "Your monthly statement is ready..."
    }
    
    # Act
    domain, details = classifier.classify_dict(email_data)
    
    # Assert
    assert domain == "finance"
    assert details["method1"]["domain"] == "finance"
    assert details["method2"]["domain"] == "finance"
    assert details["agreement"] is True
```

## 🚨 Continuous Integration

### GitHub Actions

The project includes automated testing in `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: |
          pytest --cov=email_classifier --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Quality Gates

Tests must pass these quality gates:

- **All tests pass** (100% success rate)
- **Coverage ≥ 90%** for overall codebase
- **No flaky tests** (consistent results)
- **Performance benchmarks** within limits

## 📞 Test Support

### Common Test Issues

**Test failures due to data changes:**
```bash
# Regenerate test fixtures
pytest tests/test_domains.py::test_with_fresh_data -v
```

**Memory issues in tests:**
```bash
# Reduce test dataset size
pytest tests/test_processor.py --chunk-size 100
```

**Timeout in integration tests:**
```bash
# Increase timeout or mark as slow
pytest tests/test_enhanced_statistics.py -m "not slow"
```

### Getting Help with Tests

1. **Check test logs**: `pytest -v --tb=long`
2. **Review documentation**: [Development Guide](../docs/development-playbook.md)
3. **Search issues**: [GitHub Issues](https://github.com/luongnv89/email-classifier/issues)
4. **Ask in discussions**: [GitHub Discussions](https://github.com/luongnv89/email-classifier/discussions)

---

**Related Documentation**:
- [Email Classifier Module](../email_classifier/README.md) - Module being tested
- [Development Guide](../docs/development-playbook.md) - Development setup
- [API Documentation](../docs/api/) - API reference
- [Architecture](../docs/architecture/) - System design