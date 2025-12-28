"""LLM-based email classification module.

This module provides optional LLM classification as Method 3,
complementing the existing keyword taxonomy and structural template methods.

Usage:
    from email_classifier.llm import LLMClassifier, LLMConfig

    config = LLMConfig.from_env()
    classifier = LLMClassifier(config)
    result = classifier.classify(email_data)
"""

from .agent import LLMClassifier
from .config import LLMConfig
from .schemas import DomainClassification, LLMClassificationResult

__all__ = [
    "LLMClassifier",
    "LLMConfig",
    "DomainClassification",
    "LLMClassificationResult",
]
