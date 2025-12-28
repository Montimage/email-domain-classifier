"""Pydantic models for structured LLM output."""

from pydantic import BaseModel, Field


class DomainClassification(BaseModel):
    """Classification result for a single domain."""

    domain: str = Field(
        description="The domain category name (e.g., 'finance', 'healthcare')"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0",
    )
    reasoning: str = Field(
        description="Brief explanation for why this domain was assigned"
    )


class LLMClassificationResult(BaseModel):
    """Complete LLM classification result for an email."""

    classifications: list[DomainClassification] = Field(
        description="List of domain classifications ordered by confidence (highest first)"
    )
    primary_domain: str = Field(
        description="The most confident domain classification"
    )
    analysis: str = Field(
        description="Brief analysis of the email content and classification reasoning"
    )

    def get_scores(self) -> dict[str, float]:
        """Convert classifications to a score dictionary.

        Returns:
            Dictionary mapping domain names to confidence scores.
        """
        return {c.domain: c.confidence for c in self.classifications}

    def get_highest_confidence(self) -> float:
        """Get the highest confidence score.

        Returns:
            The confidence of the primary domain, or 0.0 if no classifications.
        """
        if not self.classifications:
            return 0.0
        return self.classifications[0].confidence

    @classmethod
    def unsure(cls, reason: str = "Could not classify email") -> "LLMClassificationResult":
        """Create an 'unsure' result for fallback cases.

        Args:
            reason: Explanation for why classification failed.

        Returns:
            LLMClassificationResult with 'unsure' as primary domain.
        """
        return cls(
            classifications=[
                DomainClassification(
                    domain="unsure",
                    confidence=0.0,
                    reasoning=reason,
                )
            ],
            primary_domain="unsure",
            analysis=reason,
        )
