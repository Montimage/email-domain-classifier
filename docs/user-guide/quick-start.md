# Quick Start Guide

Get up and running with Email Domain Classifier in just 5 minutes! This guide will walk you through installation, basic usage, and understanding your first results.

## 🚀 5-Minute Quick Start

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/luongnv89/email-classifier.git
cd email-classifier

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

### Step 2: Run First Classification

```bash
# Use the provided sample data
email-classifier sample_emails.csv -o classified_emails/
```

### Step 3: View Results

```bash
# Check output files
ls -la classified_emails/

# View classification summary
cat classified_emails/classification_report.txt
```

**🎉 That's it!** You've successfully classified your first email dataset.

## 📊 Understanding Your Results

### Output Files Created

```
classified_emails/
├── email_finance.csv              # Finance-related emails
├── email_technology.csv           # Technology-related emails
├── email_retail.csv               # Retail-related emails
├── ... (other domain files)       # Other domain categories
├── email_unsure.csv               # Unclassified emails
├── classification_report.json       # Machine-readable report
├── classification_report.txt        # Human-readable report
└── classification.log              # Detailed processing log
```

### Sample Report Output

```
═══════════════════════════════════════════════════════════════════════════════
                    EMAIL CLASSIFICATION REPORT
═══════════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────────────────
  SUMMARY
────────────────────────────────────────────────────────────────────────────────────
  Total Emails Processed:  10,000
  Successfully Classified: 7,542 (75.42%)
  Unsure/Unclassified:     2,458
  Errors:                  0 (0.00%)

────────────────────────────────────────────────────────────────────────────────────
  DOMAIN BREAKDOWN
────────────────────────────────────────────────────────────────────────────────────
  💰 Finance              ██████████████████████████████    2,341 ( 23.4%)
  💻 Technology           ████████████████████░░░░░░░░░    1,876 ( 18.8%)
  🛒 Retail               ████████████████░░░░░░░░░░░░░░    1,523 ( 15.2%)
  ...
```

## 📋 Using Your Own Data

### Prepare Your CSV File

Your CSV must have these columns:

| Column | Required | Example |
|--------|----------|---------|
| `sender` | ✅ | `security@bank.com` |
| `receiver` | ✅ | `user@company.com` |
| `timestamp` | ✅ | `2024-01-15 10:30:00` |
| `subject` | ✅ | `Your account statement is ready` |
| `body` | ✅ | `Dear Customer, Your monthly statement...` |
| `has_url` | ✅ | `true`, `false`, `1`, or `0` |

### Run Classification

```bash
# Basic classification
email-classifier your_data.csv -o output/

# With detailed output and progress
email-classifier your_data.csv -o output/ --verbose --include-details

# For large files, adjust chunk size
email-classifier large_dataset.csv -o output/ --chunk-size 500
```

## 🔧 Common Options

```bash
email-classifier [OPTIONS] INPUT_FILE

Essential Options:
  -o, --output DIR          Output directory (required)
  -v, --verbose             Show detailed progress
  -q, --quiet               Suppress console output
  --include-details          Add classification scores to output
  --chunk-size INT           Adjust memory usage (default: 1000)
  --list-domains           Show all supported domains
  --help                   Show all options
```

## 🎯 What Makes This Classifier Special?

### Dual-Method Validation

Unlike simple keyword matching, our classifier uses **two independent methods**:

1. **Keyword Analysis** - Detects domain-specific terminology
2. **Structural Analysis** - Analyzes email format and patterns

**Both methods must agree** before classifying an email, ensuring high confidence and reducing false positives.

### Memory-Efficient Processing

- **Streaming processing** handles huge files without memory issues
- **Configurable chunk sizes** for different system capabilities
- **Progress tracking** for long-running operations

## 📊 Domain Categories

The classifier categorizes emails into 10 business domains:

| Domain | Examples |
|--------|----------|
| 💰 **Finance** | Bank statements, payment confirmations, insurance |
| 💻 **Technology** | Software updates, tech support, IT services |
| 🛒 **Retail** | Shopping receipts, order confirmations, promotions |
| 📦 **Logistics** | Shipping notifications, tracking updates |
| 🏥 **Healthcare** | Medical appointments, insurance claims |
| 🏛️ **Government** | Tax notices, official communications |
| 👥 **HR** | Job applications, HR notifications |
| 📞 **Telecommunications** | Bill notifications, service updates |
| 📱 **Social Media** | Platform notifications, activity updates |
| 🎓 **Education** | Course materials, academic notices |

## 🔍 Next Steps

Now that you're up and running:

1. **[Explore advanced usage](usage-examples.md)** - Learn powerful features
2. **[Check CLI reference](cli-reference.md)** - All options and flags
3. **[Read API docs](../../api/)** - Integrate with Python
4. **[Troubleshoot issues](troubleshooting.md)** - Solve common problems

## 🆘 Need Help?

```bash
# Get help with commands
email-classifier --help

# Check your installation
email-classifier --version
email-classifier --list-domains

# Test with verbose output for debugging
email-classifier sample_emails.csv -o test/ --verbose
```

---

**Ready for more?** Continue to [Usage Examples](usage-examples.md) for advanced features and real-world use cases.