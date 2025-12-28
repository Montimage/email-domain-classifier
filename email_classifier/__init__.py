"""Email Domain Classifier Package.

A Python library for classifying emails by domain using dual-method validation.
Combines keyword taxonomy matching and structural template analysis for accurate
domain classification across 10 business domains.

Main Classes:
- EmailClassifier: Main classifier combining both methods
- StreamingProcessor: Memory-efficient processing of large CSV datasets
- ClassificationReporter: Generate detailed reports and statistics

Usage:
    from email_classifier import EmailClassifier

    classifier = EmailClassifier()
    domain, details = classifier.classify_dict(email_data)
"""

# Version info
__version__ = "1.0.0"
__author__ = "Montimage Security Research"
__email__ = "research@montimage.com"

# Processing and reporting
from .analyzer import AnalysisResult, DatasetAnalyzer

# Core classification classes
from .classifier import (
    ClassificationResult,
    EmailClassifier,
    EmailData,
    KeywordTaxonomyClassifier,
    StructuralTemplateClassifier,
)

# CLI entry point
from .cli import main

# Domain definitions
from .domains import (
    DOMAINS,
    DomainProfile,
    get_all_profiles,
    get_domain_names,
    get_domain_profile,
)
from .processor import ProcessingStats, StreamingProcessor
from .reporter import ClassificationReporter, ReportConfig

# UI components
from .ui import RICH_AVAILABLE, SimpleUI, TerminalUI, get_ui

# LLM module imports (optional - only available if LLM dependencies installed)
try:
    from .llm import (
        DomainClassification,
        LLMClassificationResult,
        LLMClassifier,
        LLMConfig,
    )

    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False
    # Define placeholders for type checking
    LLMClassifier = None  # type: ignore
    LLMConfig = None  # type: ignore
    LLMClassificationResult = None  # type: ignore
    DomainClassification = None  # type: ignore


def llm_available() -> bool:
    """Check if LLM classification is available."""
    return _LLM_AVAILABLE


# Public API
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Core classes
    "EmailClassifier",
    "EmailData",
    "ClassificationResult",
    "KeywordTaxonomyClassifier",
    "StructuralTemplateClassifier",
    # LLM classes (optional)
    "LLMClassifier",
    "LLMConfig",
    "LLMClassificationResult",
    "DomainClassification",
    "llm_available",
    # Processing and Analysis
    "StreamingProcessor",
    "ProcessingStats",
    "DatasetAnalyzer",
    "AnalysisResult",
    # Reporting
    "ClassificationReporter",
    "ReportConfig",
    # Domains
    "DOMAINS",
    "DomainProfile",
    "get_domain_names",
    "get_domain_profile",
    "get_all_profiles",
    # UI
    "get_ui",
    "TerminalUI",
    "SimpleUI",
    "RICH_AVAILABLE",
    # CLI
    "main",
]
