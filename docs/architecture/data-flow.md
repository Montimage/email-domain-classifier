# Data Flow

This document describes how data flows through the Email Domain Classifier.

## Processing Pipeline

```mermaid
flowchart TD
    subgraph Input["Input Stage"]
        CSV[CSV File] --> Stream[Streaming Reader]
        Stream --> Chunk[Chunk Buffer]
    end

    subgraph Validation["Validation Stage"]
        Chunk --> Validate{Valid Email?}
        Validate -->|No| Invalid[invalid_emails.csv]
        Validate -->|Yes| Filter{Body Length OK?}
        Filter -->|No| Skipped[skipped_emails.csv]
        Filter -->|Yes| Process[Process Email]
    end

    subgraph Classification["Classification Stage"]
        Process --> Normalize[Normalize Fields]
        Normalize --> Classify[Classify Domain]
        Classify --> Enrich[Add Classification Data]
    end

    subgraph Output["Output Stage"]
        Enrich --> Route{Route by Domain}
        Route --> Finance[email_finance.csv]
        Route --> Tech[email_technology.csv]
        Route --> Retail[email_retail.csv]
        Route --> Other[email_*.csv]
        Route --> Unsure[email_unsure.csv]

        Enrich --> Stats[Update Statistics]
        Stats --> Report[Generate Reports]
    end

    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef validate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px

    class CSV,Stream,Chunk input
    class Validate,Filter,Invalid,Skipped validate
    class Process,Normalize,Classify,Enrich process
    class Route,Finance,Tech,Retail,Other,Unsure,Stats,Report output
```

## Data Transformations

### Input Normalization

| Input Column | Output Column | Transformation |
|--------------|---------------|----------------|
| `timestamp` | `date` | Renamed |
| `has_url` | `urls` | Renamed |
| `sender` | `sender` | Validated format |
| `receiver` | `receiver` | Validated format |
| `subject` | `subject` | Trimmed whitespace |
| `body` | `body` | Trimmed whitespace |

### Output Enrichment

Each processed email receives additional columns:

| Column | Description |
|--------|-------------|
| `label` | Classified domain |
| `classified_domain` | Same as label |
| `method1_domain` | Keyword method result |
| `method2_domain` | Structural method result |

### Optional Detail Columns

When `--include-details` is enabled:

| Column | Description |
|--------|-------------|
| `method1_confidence` | Keyword method confidence |
| `method2_confidence` | Structural method confidence |
| `agreement` | Whether methods agreed |

## Memory Efficiency

The streaming processor handles large files efficiently:

```mermaid
flowchart LR
    File[Large CSV] --> Chunk1[Chunk 1]
    Chunk1 --> Process1[Process]
    Process1 --> Write1[Write]
    Write1 --> Chunk2[Chunk 2]
    Chunk2 --> Process2[Process]
    Process2 --> Write2[Write]
    Write2 --> ChunkN[Chunk N...]

    classDef file fill:#e3f2fd,stroke:#1976d2
    classDef chunk fill:#f3e5f5,stroke:#7b1fa2
    classDef action fill:#e8f5e9,stroke:#388e3c

    class File file
    class Chunk1,Chunk2,ChunkN chunk
    class Process1,Process2,Write1,Write2 action
```

- **Default Chunk Size**: 1000 emails
- **Memory Usage**: ~2MB per 1000 emails
- **Configurable**: `--chunk-size` CLI option

## Related Documentation

- [Architecture Overview](overview.md)
- [Classification Flow](classification-flow.md)
- [Installation Guide](../integration/installation.md)
