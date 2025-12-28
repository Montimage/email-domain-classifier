"""LLM-based email classifier using LangGraph agent architecture."""

import logging
from typing import Any, Optional

from ..classifier import ClassificationResult, EmailData
from ..domains import get_domain_names
from .config import LLMConfig, LLMConfigError
from .prompts import get_classification_prompt, get_system_prompt
from .providers import ProviderNotInstalledError, create_llm
from .schemas import DomainClassification, LLMClassificationResult

logger = logging.getLogger(__name__)


class LLMClassifier:
    """LLM-based email classifier (Method 3).

    Uses LangChain/LangGraph to classify emails into domain categories
    using semantic analysis. Supports multiple LLM providers.
    """

    def __init__(self, config: LLMConfig) -> None:
        """Initialize the LLM classifier.

        Args:
            config: LLM configuration with provider, model, and settings.

        Raises:
            ProviderNotInstalledError: If the provider package is not installed.
            LLMConfigError: If configuration is invalid.
        """
        self.config = config
        self._llm: Optional[Any] = None
        self._structured_llm: Optional[Any] = None
        self._valid_domains = set(get_domain_names()) | {"unsure"}

    def _get_llm(self) -> Any:
        """Get or create the LLM instance (lazy initialization).

        Returns:
            LangChain-compatible LLM instance.
        """
        if self._llm is None:
            self._llm = create_llm(self.config)
        return self._llm

    def _get_structured_llm(self) -> Any:
        """Get LLM with structured output for classification results.

        Returns:
            LLM configured for structured LLMClassificationResult output.
        """
        if self._structured_llm is None:
            llm = self._get_llm()
            self._structured_llm = llm.with_structured_output(LLMClassificationResult)
        return self._structured_llm

    def classify(self, email: EmailData) -> ClassificationResult:
        """Classify an email using LLM semantic analysis.

        Args:
            email: Email data to classify.

        Returns:
            ClassificationResult with domain, confidence, and scores.
        """
        try:
            result = self._invoke_llm(email)
            return self._convert_to_classification_result(result)
        except Exception as e:
            logger.warning(f"LLM classification failed: {e}")
            return self._create_fallback_result(str(e))

    def _invoke_llm(self, email: EmailData) -> LLMClassificationResult:
        """Invoke the LLM to classify an email.

        Args:
            email: Email data to classify.

        Returns:
            Structured LLM classification result.

        Raises:
            Exception: If LLM invocation fails after retries.
        """
        structured_llm = self._get_structured_llm()
        system_prompt = get_system_prompt()
        user_prompt = get_classification_prompt(
            sender=email.sender,
            subject=email.subject,
            body=email.body,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        last_error: Optional[Exception] = None
        for attempt in range(self.config.retry_count + 1):
            try:
                result = structured_llm.invoke(messages)
                return self._validate_result(result)
            except Exception as e:
                last_error = e
                logger.debug(
                    f"LLM attempt {attempt + 1}/{self.config.retry_count + 1} failed: {e}"
                )
                if attempt < self.config.retry_count:
                    continue
                raise

        # Should not reach here, but handle gracefully
        raise last_error or Exception("LLM invocation failed")

    def _validate_result(self, result: LLMClassificationResult) -> LLMClassificationResult:
        """Validate and normalize the LLM result.

        Args:
            result: Raw LLM classification result.

        Returns:
            Validated and normalized result.
        """
        # Normalize domain names to match our known domains
        valid_classifications = []
        for classification in result.classifications:
            domain = classification.domain.lower().strip()
            # Map common variations
            domain = self._normalize_domain_name(domain)
            if domain in self._valid_domains:
                valid_classifications.append(
                    DomainClassification(
                        domain=domain,
                        confidence=max(0.0, min(1.0, classification.confidence)),
                        reasoning=classification.reasoning,
                    )
                )

        # Ensure we have at least one classification
        if not valid_classifications:
            valid_classifications = [
                DomainClassification(
                    domain="unsure",
                    confidence=0.3,
                    reasoning="LLM returned no valid domain classifications",
                )
            ]

        # Sort by confidence
        valid_classifications.sort(key=lambda c: c.confidence, reverse=True)

        # Determine primary domain
        primary_domain = valid_classifications[0].domain

        return LLMClassificationResult(
            classifications=valid_classifications,
            primary_domain=primary_domain,
            analysis=result.analysis,
        )

    def _normalize_domain_name(self, domain: str) -> str:
        """Normalize domain name variations.

        Args:
            domain: Raw domain name from LLM.

        Returns:
            Normalized domain name matching our taxonomy.
        """
        # Map common variations to our domain names
        domain_map = {
            "human_resources": "hr",
            "human resources": "hr",
            "humanresources": "hr",
            "telecom": "telecommunications",
            "telco": "telecommunications",
            "social": "social_media",
            "socialmedia": "social_media",
            "banking": "finance",
            "financial": "finance",
            "medical": "healthcare",
            "health": "healthcare",
            "gov": "government",
            "govt": "government",
            "shopping": "retail",
            "ecommerce": "retail",
            "e-commerce": "retail",
            "shipping": "logistics",
            "delivery": "logistics",
            "tech": "technology",
            "software": "technology",
            "school": "education",
            "university": "education",
            "college": "education",
        }
        return domain_map.get(domain, domain)

    def _convert_to_classification_result(
        self, llm_result: LLMClassificationResult
    ) -> ClassificationResult:
        """Convert LLM result to standard ClassificationResult.

        Args:
            llm_result: LLM classification result.

        Returns:
            Standard ClassificationResult compatible with other methods.
        """
        # Build scores dictionary from all valid domains
        scores = {}
        for domain_name in get_domain_names():
            scores[domain_name] = 0.0

        # Fill in scores from LLM classifications
        for classification in llm_result.classifications:
            if classification.domain in scores:
                scores[classification.domain] = classification.confidence

        # Get primary domain and confidence
        domain = llm_result.primary_domain
        confidence = llm_result.get_highest_confidence()

        # If primary domain is unsure, set domain to None for consistency
        if domain == "unsure":
            domain = None
            confidence = 0.0

        return ClassificationResult(
            domain=domain,
            confidence=confidence,
            scores=scores,
            method="llm_agent",
            details={
                "analysis": llm_result.analysis,
                "classifications": [
                    {
                        "domain": c.domain,
                        "confidence": c.confidence,
                        "reasoning": c.reasoning,
                    }
                    for c in llm_result.classifications
                ],
                "provider": self.config.provider.value,
                "model": self.config.model,
            },
        )

    def _create_fallback_result(self, error_message: str) -> ClassificationResult:
        """Create a fallback result when LLM fails.

        Args:
            error_message: Description of the failure.

        Returns:
            ClassificationResult indicating LLM failure.
        """
        scores = {domain: 0.0 for domain in get_domain_names()}

        return ClassificationResult(
            domain=None,
            confidence=0.0,
            scores=scores,
            method="llm_agent",
            details={
                "error": error_message,
                "fallback": True,
            },
        )

    @classmethod
    def from_env(cls) -> "LLMClassifier":
        """Create an LLMClassifier from environment configuration.

        Returns:
            Configured LLMClassifier instance.

        Raises:
            LLMConfigError: If configuration is invalid.
            ProviderNotInstalledError: If provider package not installed.
        """
        config = LLMConfig.from_env()
        return cls(config)
