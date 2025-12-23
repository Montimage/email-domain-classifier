# Common Issues

This guide covers common issues and their solutions.

## Installation Issues

### Python Version Mismatch

**Problem**: `ModuleNotFoundError` or syntax errors

**Solution**:
```bash
# Check Python version (requires 3.10+)
python --version

# Use specific version
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Permission Denied

**Problem**: `PermissionError` during installation

**Solution**:
```bash
# Use user installation
pip install --user -e .

# Or fix permissions
sudo chown -R $USER ~/.local
```

### Rich Library Issues

**Problem**: Terminal output looks broken

**Solution**:
```bash
# Reinstall rich
pip uninstall rich
pip install rich>=13.0.0

# Check terminal support
python -c "from rich.console import Console; Console().print('[bold green]Rich works![/]')"
```

## Runtime Issues

### Memory Errors

**Problem**: `MemoryError` with large files

**Solution**:
```bash
# Reduce chunk size
email-cli large_file.csv -o output/ --chunk-size 500

# Process in parts
head -n 100000 large_file.csv > part1.csv
email-cli part1.csv -o output/
```

### Slow Processing

**Problem**: Classification takes too long

**Solution**:
```bash
# Increase chunk size for faster I/O
email-cli data.csv -o output/ --chunk-size 2000

# Check for very long emails
email-cli info data.csv  # View body length distribution
email-cli data.csv -o output/ --max-body-length 5000
```

### Invalid Email Errors

**Problem**: Many emails marked as invalid

**Solution**:
```bash
# Check validation errors
cat output/invalid_emails.csv | head

# Common issues:
# - Empty sender/receiver: Check CSV formatting
# - Invalid email format: Verify data quality
# - Empty body: Some emails may be notifications only
```

## Output Issues

### Missing Output Files

**Problem**: No CSV files generated

**Solution**:
```bash
# Check output directory
ls -la output/

# Verify input file has data
wc -l input.csv
head input.csv

# Check for processing errors in log
cat output/classification.log
```

### All Emails Marked Unsure

**Problem**: Everything classified as "unsure"

**Causes**:
1. Methods disagree on domain
2. Confidence scores too low
3. Emails don't match any domain profile

**Solution**:
```bash
# Analyze dataset first
email-cli info data.csv

# Check label distribution
# If emails are very diverse, classification may be difficult
```

### Incorrect Classifications

**Problem**: Emails assigned to wrong domain

**Solution**:
```bash
# Use detailed output to debug
email-cli data.csv -o output/ --include-details

# Check method agreement in output
# method1_domain, method2_domain columns show individual results
```

## CSV Format Issues

### Column Not Found

**Problem**: `KeyError` for expected columns

**Solution**:
```bash
# Check column names
head -1 input.csv

# Expected columns:
# sender, receiver, subject, body
# Optional: date/timestamp, urls/has_url, label
```

### Encoding Errors

**Problem**: `UnicodeDecodeError`

**Solution**:
```bash
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.csv > input_utf8.csv

# Or specify encoding in Python
# (future feature)
```

### CSV Parsing Errors

**Problem**: Malformed CSV data

**Solution**:
```bash
# Validate CSV format
python -c "import csv; list(csv.reader(open('input.csv')))"

# Common fixes:
# - Ensure proper quoting for fields with commas
# - Remove or escape embedded quotes
# - Check for consistent column count
```

## Related Documentation

- [FAQ](faq.md)
- [Installation Guide](../integration/installation.md)
- [User Guide](../user-guide/quick-start.md)
