# Design: Domain Profiles

This document describes the domain profile system used for email classification.

## Domain Profile Structure

Each domain is defined by a `DomainProfile` dataclass:

```mermaid
classDiagram
    class DomainProfile {
        +str name
        +str display_name
        +str color
        +Set~str~ primary_keywords
        +Set~str~ secondary_keywords
        +List~str~ sender_patterns
        +List~str~ subject_patterns
        +Tuple typical_body_length
        +bool has_greeting
        +bool has_signature
        +bool has_disclaimer
        +bool url_expected
        +str formality_level
        +Tuple typical_paragraph_count
    }

    class KeywordTaxonomy {
        primary_keywords
        secondary_keywords
        sender_patterns
        subject_patterns
    }

    class StructuralTemplate {
        typical_body_length
        has_greeting
        has_signature
        has_disclaimer
        url_expected
        formality_level
        typical_paragraph_count
    }

    DomainProfile --> KeywordTaxonomy : Method 1
    DomainProfile --> StructuralTemplate : Method 2
```

## Supported Domains

| Domain | Display Name | Formality | URL Expected |
|--------|--------------|-----------|--------------|
| `finance` | Finance | Formal | Yes |
| `technology` | Technology | Semi-formal | Yes |
| `retail` | Retail | Semi-formal | Yes |
| `logistics` | Logistics | Formal | Yes |
| `healthcare` | Healthcare | Formal | No |
| `government` | Government | Formal | No |
| `hr` | HR | Formal | No |
| `telecommunications` | Telecom | Semi-formal | Yes |
| `social_media` | Social Media | Casual | Yes |
| `education` | Education | Semi-formal | Yes |

## Profile Components

### Keyword Taxonomy (Method 1)

```mermaid
flowchart LR
    subgraph Primary["Primary Keywords (High Weight)"]
        P1[account]
        P2[payment]
        P3[transaction]
    end

    subgraph Secondary["Secondary Keywords (Medium Weight)"]
        S1[balance]
        S2[statement]
        S3[banking]
    end

    subgraph Patterns["Pattern Matching"]
        SP[Sender: *@bank.com]
        SUB[Subject: *statement*]
    end

    Primary --> Score[Domain Score]
    Secondary --> Score
    Patterns --> Score

    classDef primary fill:#e3f2fd,stroke:#1976d2
    classDef secondary fill:#f3e5f5,stroke:#7b1fa2
    classDef pattern fill:#fff3e0,stroke:#f57c00

    class P1,P2,P3 primary
    class S1,S2,S3 secondary
    class SP,SUB pattern
```

### Structural Template (Method 2)

| Attribute | Finance Example | Social Media Example |
|-----------|----------------|---------------------|
| Body Length | 500-2000 chars | 100-500 chars |
| Has Greeting | Yes | No |
| Has Signature | Yes | No |
| Has Disclaimer | Yes | No |
| Formality | Formal | Casual |
| Paragraphs | 3-6 | 1-2 |

## Adding New Domains

To add a new domain, define a profile in `domains.py`:

```python
DOMAINS["new_domain"] = DomainProfile(
    name="new_domain",
    display_name="New Domain",
    color="bright_cyan",
    # Keyword Taxonomy
    primary_keywords={"keyword1", "keyword2"},
    secondary_keywords={"support1", "support2"},
    sender_patterns=[r".*@newdomain\.com"],
    subject_patterns=[r".*new.*"],
    # Structural Template
    typical_body_length=(200, 1000),
    has_greeting=True,
    has_signature=True,
    has_disclaimer=False,
    url_expected=True,
    formality_level="semi-formal",
    typical_paragraph_count=(2, 4),
)
```

## Related Documentation

- [Dual-Method Validation](dual-method-validation.md)
- [Classification Flow](../architecture/classification-flow.md)
