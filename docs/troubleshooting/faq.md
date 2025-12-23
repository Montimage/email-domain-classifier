# Frequently Asked Questions

## General Questions

### What is Email Domain Classifier?

A Python CLI tool that classifies emails into business domains (Finance, Technology, Retail, etc.) using dual-method validation for high accuracy.

### What Python versions are supported?

Python 3.10, 3.11, and 3.12 are supported. Python 3.11+ is recommended for best performance.

### Is it free to use?

Yes, the project is licensed under Apache License 2.0.

## Classification Questions

### How does dual-method validation work?

Two independent classification methods analyze each email:
1. **Keyword Taxonomy** (60% weight) - Analyzes content keywords
2. **Structural Templates** (40% weight) - Analyzes email structure

Classification only occurs when both methods agree on the domain.

### Why are emails marked as "unsure"?

Emails are marked unsure when:
- Methods disagree on the domain
- Combined confidence score is below threshold (0.15)
- Email doesn't match any domain profile well

### Can I add custom domains?

Yes, add domain profiles to `domains.py`. See [Domain Profiles](../design/domain-profiles.md) documentation.

### What domains are supported?

10 business domains: Finance, Technology, Retail, Logistics, Healthcare, Government, HR, Telecommunications, Social Media, and Education.

## Input/Output Questions

### What CSV format is required?

Required columns: `sender`, `receiver`, `subject`, `body`

Optional columns: `date`/`timestamp`, `urls`/`has_url`, `label`

### What outputs are generated?

- `email_[domain].csv` - Classified emails by domain
- `email_unsure.csv` - Emails that couldn't be confidently classified
- `invalid_emails.csv` - Emails that failed validation
- `skipped_emails.csv` - Emails filtered (e.g., body too long)
- `classification_report.json` - Detailed statistics
- `classification_report.txt` - Human-readable summary

### How large can input files be?

The streaming processor handles files of any size with constant memory usage. Tested with 10M+ emails.

### Can I filter emails by body length?

Yes, use `--max-body-length`:
```bash
email-cli emails.csv -o output/ --max-body-length 2000
```

## Performance Questions

### How fast is classification?

Typical speed: 1,000-5,000 emails/second depending on:
- Email body length
- Disk I/O speed
- Chunk size setting

### How can I speed up processing?

```bash
# Increase chunk size
email-cli data.csv -o output/ --chunk-size 2000

# Filter long emails
email-cli data.csv -o output/ --max-body-length 5000

# Use SSD storage for I/O
```

### What is the memory usage?

Memory usage scales with chunk size, not file size:
- Default (1000 emails): ~100MB
- Large chunks (5000): ~500MB

## Validation Questions

### What does email validation check?

- Sender/receiver have valid email format
- Subject is not empty
- Body is not empty or whitespace-only

### What happens to invalid emails?

Invalid emails are skipped and logged to `invalid_emails.csv` with error reasons.

### Can I fail on first invalid email?

Yes, use `--strict-validation`:
```bash
email-cli data.csv -o output/ --strict-validation
```

## Development Questions

### How do I run tests?

```bash
pytest --cov=email_classifier
```

### How do I contribute?

See [Development Playbook](../playbooks/development-playbook.md) for setup and contribution guidelines.

### Where do I report bugs?

Open an issue on [GitHub Issues](https://github.com/montimage/email-domain-classifier/issues).

## Related Documentation

- [Common Issues](common-issues.md)
- [Quick Start Guide](../user-guide/quick-start.md)
- [Installation Guide](../integration/installation.md)
