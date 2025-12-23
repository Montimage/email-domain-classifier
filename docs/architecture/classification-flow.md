# Classification Flow

This document describes the email classification process in detail.

## Classification Pipeline

```mermaid
flowchart TD
    Email[Email Input] --> Extract[Extract Features]

    Extract --> M1[Method 1: Keyword Taxonomy]
    Extract --> M2[Method 2: Structural Templates]

    M1 --> Score1[Domain Scores]
    M2 --> Score2[Domain Scores]

    Score1 --> Compare{Methods Agree?}
    Score2 --> Compare

    Compare -->|Yes| Threshold{Score > 0.15?}
    Compare -->|No| Unsure[Mark as Unsure]

    Threshold -->|Yes| Classify[Assign Domain]
    Threshold -->|No| Unsure

    Classify --> Output[Output Result]
    Unsure --> Output

    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px

    class Email input
    class Extract,M1,M2,Score1,Score2 process
    class Compare,Threshold decision
    class Classify,Unsure,Output output
```

## Method 1: Keyword Taxonomy (60% Weight)

Analyzes email content against domain-specific keyword taxonomies:

| Factor | Description | Weight |
|--------|-------------|--------|
| Primary Keywords | Core domain terms | High |
| Secondary Keywords | Supporting terms | Medium |
| Sender Patterns | Email domain patterns | Medium |
| Subject Patterns | Subject line patterns | Low |

## Method 2: Structural Templates (40% Weight)

Analyzes email structure and format:

| Factor | Description |
|--------|-------------|
| Body Length | Typical character range for domain |
| Greeting | Presence of formal greeting |
| Signature | Presence of signature block |
| Disclaimer | Presence of legal disclaimer |
| Formality | Formal, semi-formal, or casual |
| Paragraph Count | Typical structure for domain |

## Agreement Requirement

Classification requires **both methods to agree** on the top domain:

```mermaid
flowchart LR
    M1[Method 1: Finance] --> Check{Same Domain?}
    M2[Method 2: Finance] --> Check
    Check -->|Yes| Confident[High Confidence]
    Check -->|No| Unsure[Mark Unsure]

    classDef method fill:#f3e5f5,stroke:#7b1fa2
    classDef decision fill:#fff3e0,stroke:#f57c00
    classDef result fill:#e8f5e9,stroke:#388e3c

    class M1,M2 method
    class Check decision
    class Confident,Unsure result
```

## Confidence Threshold

- **Minimum Score**: 0.15 combined confidence
- **Combined Score**: `(Method1 * 0.6) + (Method2 * 0.4)`

## Related Documentation

- [Architecture Overview](overview.md)
- [Data Flow](data-flow.md)
- [Domain Profiles](../design/domain-profiles.md)
