# Architecture Overview

The Email Domain Classifier is a Python-based system for classifying emails into business domains using dual-method validation.

## System Architecture

```mermaid
flowchart TD
    subgraph Input["Input Layer"]
        CSV[CSV File]
        CLI[CLI Interface]
    end

    subgraph Processing["Processing Layer"]
        Validator[Email Validator]
        Processor[Streaming Processor]
        Classifier[Email Classifier]
    end

    subgraph Classification["Classification Engine"]
        Method1[Keyword Taxonomy]
        Method2[Structural Templates]
        Combiner[Score Combiner]
    end

    subgraph Output["Output Layer"]
        DomainCSV[Domain CSV Files]
        Reports[JSON/Text Reports]
        Invalid[Invalid Emails Log]
        Skipped[Skipped Emails Log]
    end

    CSV --> CLI
    CLI --> Validator
    Validator --> Processor
    Processor --> Classifier

    Classifier --> Method1
    Classifier --> Method2
    Method1 --> Combiner
    Method2 --> Combiner

    Combiner --> DomainCSV
    Combiner --> Reports
    Validator --> Invalid
    Processor --> Skipped

    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px

    class CSV,CLI input
    class Validator,Processor,Classifier,Method1,Method2,Combiner process
    class DomainCSV,Reports,Invalid,Skipped output
```

## Core Components

| Component | Module | Responsibility |
|-----------|--------|----------------|
| **CLI** | `cli.py` | Command-line interface, argument parsing |
| **Validator** | `validator.py` | Email format validation, data quality checks |
| **Processor** | `processor.py` | Streaming CSV processing, memory efficiency |
| **Classifier** | `classifier.py` | Dual-method classification engine |
| **Domains** | `domains.py` | Domain profiles and keyword taxonomies |
| **Reporter** | `reporter.py` | Report generation (JSON, text) |
| **UI** | `ui.py` | Terminal UI with Rich library |
| **Analyzer** | `analyzer.py` | Dataset analysis (info command) |

## Design Principles

1. **Streaming Processing** - Memory-efficient handling of large datasets
2. **Dual-Method Validation** - High confidence through method agreement
3. **Extensible Domains** - Easy addition of new business domains
4. **Rich Terminal UI** - Beautiful progress bars and formatted output

## Related Documentation

- [Classification Flow](classification-flow.md) - Detailed classification process
- [Data Flow](data-flow.md) - Data processing pipeline
- [Design: Dual-Method Validation](../design/dual-method-validation.md) - Classification design decisions
