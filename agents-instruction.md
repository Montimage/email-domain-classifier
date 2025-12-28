# AI-Agent Project Setup Instructions

This document provides step-by-step instructions for AI coding assistants to automatically set up the email-domain-classifier project.

## Default Configuration

Use these defaults without prompting the user:

| Setting | Default Value |
|---------|---------------|
| Setup type | Basic usage |
| LLM enabled | Yes |
| LLM provider | Ollama (local) |
| LLM model | llama3.1:8b |
| Temperature | 0.0 |
| Max tokens | 1024 |
| Ollama URL | http://localhost:11434 |

---

## Step 1: System Prerequisites

### 1.1 Check Python Version

```bash
python3 --version
```

**Expected**: Python 3.10, 3.11, or 3.12

**If missing or below 3.10**: Inform user to install Python:
- macOS: `brew install python@3.11`
- Ubuntu/Debian: `sudo apt install python3.11 python3.11-venv`
- Windows: Download from https://python.org

### 1.2 Check Git

```bash
git --version
```

**If missing**: Inform user to install Git from https://git-scm.com

### 1.3 Check pip

```bash
python3 -m pip --version
```

**If missing**: Run `python3 -m ensurepip --upgrade`

---

## Step 2: Project Repository

### 2.1 Verify Existing Repository

Check if already in the project directory:

```bash
test -f pyproject.toml && grep -q "email-domain-classifier" pyproject.toml && echo "OK"
```

**If OK**: Proceed to Step 3

### 2.2 Clone Repository (if needed)

```bash
git clone https://github.com/montimage/email-domain-classifier.git
cd email-domain-classifier
```

---

## Step 3: Virtual Environment

### 3.1 Check for Existing Environment

```bash
test -d .venv && echo "EXISTS" || echo "NOT_FOUND"
```

### 3.2 Create Virtual Environment (if not exists)

```bash
python3 -m venv .venv
```

### 3.3 Activate Virtual Environment

**Unix/macOS**:
```bash
source .venv/bin/activate
```

**Windows**:
```cmd
.venv\Scripts\activate
```

---

## Step 4: Install Dependencies

### 4.1 Upgrade pip

```bash
pip install --upgrade pip
```

### 4.2 Install Base Package

```bash
pip install -e .
```

### 4.3 Install Ollama Provider (default LLM)

```bash
pip install -e ".[ollama]"
```

### 4.4 Verify Installation

```bash
email-cli --help
```

**Expected**: Help output showing usage information

---

## Step 5: Configure LLM

### 5.1 Check Ollama Installation

```bash
ollama --version
```

**If missing**: Note in final summary - user needs to install from https://ollama.ai/download

### 5.2 Check Ollama Service

```bash
curl -s http://localhost:11434/api/tags > /dev/null && echo "RUNNING" || echo "NOT_RUNNING"
```

**If NOT_RUNNING**: Note in final summary - user needs to run `ollama serve`

### 5.3 Pull Default Model

```bash
ollama pull llama3.1:8b
```

**If Ollama not running**: Skip and note in final summary

### 5.4 Verify Model

```bash
ollama list | grep -q "llama3.1:8b" && echo "MODEL_OK" || echo "MODEL_MISSING"
```

---

## Step 6: Create Configuration File

### 6.1 Check Existing .env

```bash
test -f .env && echo "EXISTS" || echo "NOT_FOUND"
```

### 6.2 Create .env from Template

**If .env does not exist**:

```bash
cp .env.example .env
```

The `.env.example` already has correct defaults:
- `LLM_PROVIDER=ollama`
- `LLM_MODEL=llama3.1:8b`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `LLM_TEMPERATURE=0.0`

### 6.3 Update .env (if needed)

If .env exists but missing keys, add only missing ones without overwriting.

---

## Step 7: Verification

### 7.1 Verify CLI

```bash
email-cli --help
```

### 7.2 Verify Python Import

```bash
python -c "from email_classifier import EmailClassifier; print('Import OK')"
```

### 7.3 Verify LLM Connection (if Ollama running)

```bash
curl -s http://localhost:11434/api/tags | grep -q "llama3.1:8b" && echo "LLM OK"
```

---

## Step 8: Present Final Summary

After completing all steps, present this summary to the user:

```
Setup Complete! Please verify your configuration:

Configuration:
  - LLM Provider: Ollama (local)
  - LLM Model: llama3.1:8b
  - Ollama URL: http://localhost:11434
  - Config file: .env

Quick Start:
  email-cli input.csv -o output/          # Basic classification
  email-cli input.csv -o output/ --use-llm  # With LLM classification

To change settings, edit .env:
  - LLM_PROVIDER: ollama, google, mistral, groq, openrouter
  - LLM_MODEL: model name (e.g., llama3.1:8b, gemini-2.0-flash)
  - For cloud providers, add your API key
```

### Report Issues (if any)

List any issues encountered with actionable steps:

| Issue | Action |
|-------|--------|
| Ollama not installed | Install from https://ollama.ai/download |
| Ollama not running | Start with: `ollama serve` |
| Model not pulled | Run: `ollama pull llama3.1:8b` |
| Python < 3.10 | Upgrade Python to 3.10+ |

---

## Optional: Development Setup

Only if user explicitly requests development setup:

### Install Dev Dependencies

```bash
pip install -e ".[dev]"
```

### Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

### Install Security Tools

```bash
pip install detect-secrets pip-audit bandit
```

### Verify Dev Tools

```bash
pytest --version
black --version
mypy --version
```

### Run Tests

```bash
pytest tests/ --co
```

---

## Error Recovery

### Network Failure

If pip install fails:
1. Check internet connectivity
2. Try: `pip install --timeout 60 -e .`
3. Manual fallback: Download dependencies separately

### Permission Denied

If permission errors occur:
1. Try: `pip install --user -e .`
2. Check directory permissions
3. Ensure virtual environment is activated

### Ollama Connection Failed

If Ollama is unreachable:
1. Verify Ollama is installed: `ollama --version`
2. Start Ollama: `ollama serve`
3. Check port 11434 is not blocked
4. Fallback: Use dual-method classification without LLM

---

## Quick Reference

### Minimum Commands for Setup

```bash
# 1. Create and activate venv
python3 -m venv .venv && source .venv/bin/activate

# 2. Install package with Ollama support
pip install -e ".[ollama]"

# 3. Create config
cp .env.example .env

# 4. Pull model (if Ollama running)
ollama pull llama3.1:8b

# 5. Verify
email-cli --help
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| LLM_PROVIDER | ollama | LLM provider (ollama/google/mistral/groq/openrouter) |
| LLM_MODEL | llama3.1:8b | Model name |
| LLM_TEMPERATURE | 0.0 | Generation temperature |
| LLM_MAX_TOKENS | 1024 | Max response tokens |
| LLM_TIMEOUT | 30 | Request timeout (seconds) |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama API endpoint |
