"""
Email classifier implementing two classification methods:
- Method 1: Keyword Taxonomy Matching
- Method 2: Structural Template Matching
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .domains import DOMAINS, DomainProfile, get_domain_names


@dataclass
class ClassificationResult:
    """Result of a single classification method."""

    domain: Optional[str]
    confidence: float
    scores: Dict[str, float]
    method: str
    details: Dict[str, any] = None


@dataclass
class EmailData:
    """Parsed email data structure."""

    sender: str
    receiver: str
    date: str
    subject: str
    body: str
    urls: str

    @property
    def has_url(self) -> bool:
        """Compatibility property for classification logic."""
        return bool(self.urls and self.urls.strip())

    @classmethod
    def from_dict(cls, data: Dict) -> "EmailData":
        """Create EmailData from dictionary."""
        # Handle both 'urls' and 'has_url' fields
        urls_value = data.get("urls", "")
        if not urls_value and "has_url" in data:
            # Convert has_url boolean to string representation
            urls_value = "true" if data.get("has_url") else ""

        return cls(
            sender=str(data.get("sender", "")).lower().strip(),
            receiver=str(data.get("receiver", "")).lower().strip(),
            date=str(data.get("date", "")).strip(),
            subject=str(data.get("subject", "")).strip(),
            body=str(data.get("body", "")).strip(),
            urls=str(urls_value).strip(),
        )


class KeywordTaxonomyClassifier:
    """
    Method 1: Keyword Taxonomy Matching

    Scores emails based on keyword frequency and pattern matching
    against domain-specific taxonomies.
    """

    # Weights for different scoring components
    WEIGHTS = {
        "primary_keyword": 3.0,
        "secondary_keyword": 1.5,
        "sender_pattern": 4.0,
        "subject_pattern": 3.5,
        "subject_keyword": 2.5,
        "body_keyword_density": 2.0,
    }

    def __init__(self, domains: Dict[str, DomainProfile] = None):
        self.domains = domains or DOMAINS
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self._sender_patterns = {}
        self._subject_patterns = {}

        for name, profile in self.domains.items():
            self._sender_patterns[name] = [
                re.compile(p, re.IGNORECASE) for p in profile.sender_patterns
            ]
            self._subject_patterns[name] = [
                re.compile(p, re.IGNORECASE) for p in profile.subject_patterns
            ]

    def classify(self, email: EmailData) -> ClassificationResult:
        """Classify email using keyword taxonomy method."""
        scores = {}
        details = {}

        for domain_name, profile in self.domains.items():
            score, domain_details = self._score_domain(email, domain_name, profile)
            scores[domain_name] = score
            details[domain_name] = domain_details

        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            normalized = {k: v / total for k, v in scores.items()}
        else:
            normalized = scores

        # Find best match
        if scores:
            best_domain = max(scores, key=scores.get)
            best_score = scores[best_domain]
            confidence = normalized.get(best_domain, 0)

            # Require minimum confidence threshold
            if confidence < 0.05 or best_score < 1.5:
                best_domain = None
                confidence = 0.0
        else:
            best_domain = None
            confidence = 0.0

        return ClassificationResult(
            domain=best_domain,
            confidence=confidence,
            scores=normalized,
            method="keyword_taxonomy",
            details=details,
        )

    def _score_domain(
        self, email: EmailData, domain_name: str, profile: DomainProfile
    ) -> Tuple[float, Dict]:
        """Calculate score for a specific domain."""
        score = 0.0
        details = {
            "primary_matches": [],
            "secondary_matches": [],
            "sender_match": False,
            "subject_pattern_match": False,
        }

        # Check sender patterns
        for pattern in self._sender_patterns[domain_name]:
            if pattern.match(email.sender):
                score += self.WEIGHTS["sender_pattern"]
                details["sender_match"] = True
                break

        # Check subject patterns
        for pattern in self._subject_patterns[domain_name]:
            if pattern.search(email.subject):
                score += self.WEIGHTS["subject_pattern"]
                details["subject_pattern_match"] = True
                break

        # Check subject keywords
        subject_lower = email.subject.lower()
        for keyword in profile.primary_keywords:
            if keyword in subject_lower:
                score += self.WEIGHTS["subject_keyword"]
                details["primary_matches"].append(f"subject:{keyword}")

        # Check body keywords
        body_lower = email.body.lower()
        body_words = len(body_lower.split())

        primary_count = 0
        for keyword in profile.primary_keywords:
            if keyword in body_lower:
                primary_count += body_lower.count(keyword)
                details["primary_matches"].append(f"body:{keyword}")

        secondary_count = 0
        for keyword in profile.secondary_keywords:
            if keyword in body_lower:
                secondary_count += body_lower.count(keyword)
                details["secondary_matches"].append(keyword)

        # Calculate keyword density score
        if body_words > 0:
            primary_density = (primary_count / body_words) * 100
            secondary_density = (secondary_count / body_words) * 100

            score += min(primary_density * self.WEIGHTS["primary_keyword"], 15)
            score += min(secondary_density * self.WEIGHTS["secondary_keyword"], 8)

        return score, details


class StructuralTemplateClassifier:
    """
    Method 2: Structural Template Matching

    Analyzes email structure and format characteristics
    to match against domain templates.
    """

    # Structural feature weights
    WEIGHTS = {
        "body_length": 2.0,
        "greeting": 1.5,
        "signature": 1.5,
        "disclaimer": 2.0,
        "url_match": 2.5,
        "formality": 2.0,
        "paragraph_count": 1.5,
        "sender_structure": 2.5,
    }

    # Greeting patterns
    GREETING_PATTERNS = [
        re.compile(
            r"^(dear|hello|hi|greetings|good\s+(morning|afternoon|evening))",
            re.IGNORECASE | re.MULTILINE,
        ),
    ]

    # Signature patterns
    SIGNATURE_PATTERNS = [
        re.compile(
            r"(sincerely|regards|best|thank you|thanks|cheers),?\s*\n", re.IGNORECASE
        ),
        re.compile(r"\n[-–—]{2,}\s*\n", re.MULTILINE),
        re.compile(r"(sent from my|get outlook)", re.IGNORECASE),
    ]

    # Disclaimer patterns
    DISCLAIMER_PATTERNS = [
        re.compile(
            r"(confidential|disclaimer|privileged|intended recipient)", re.IGNORECASE
        ),
        re.compile(r"(this (email|message|communication) (is|may be))", re.IGNORECASE),
        re.compile(r"(do not (distribute|forward|share))", re.IGNORECASE),
    ]

    # Formality indicators
    FORMAL_INDICATORS = [
        "pursuant",
        "hereby",
        "aforementioned",
        "regarding",
        "enclosed",
        "please find",
        "kindly",
        "respectfully",
        "we regret",
        "be advised",
    ]

    CASUAL_INDICATORS = [
        "hey",
        "thanks!",
        "awesome",
        "cool",
        "btw",
        "fyi",
        "asap",
        "gonna",
        "wanna",
        "gotta",
        ":)",
        "!!",
    ]

    def __init__(self, domains: Dict[str, DomainProfile] = None):
        self.domains = domains or DOMAINS

    def classify(self, email: EmailData) -> ClassificationResult:
        """Classify email using structural template matching."""
        # Extract structural features
        features = self._extract_features(email)

        scores = {}
        details = {}

        for domain_name, profile in self.domains.items():
            score, domain_details = self._score_template_match(features, profile)
            scores[domain_name] = score
            details[domain_name] = domain_details

        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            normalized = {k: v / total for k, v in scores.items()}
        else:
            normalized = scores

        # Find best match
        if scores:
            best_domain = max(scores, key=scores.get)
            best_score = scores[best_domain]
            confidence = normalized.get(best_domain, 0)

            # Require minimum threshold
            if confidence < 0.04 or best_score < 2.0:
                best_domain = None
                confidence = 0.0
        else:
            best_domain = None
            confidence = 0.0

        return ClassificationResult(
            domain=best_domain,
            confidence=confidence,
            scores=normalized,
            method="structural_template",
            details={"features": features, "domain_scores": details},
        )

    def _extract_features(self, email: EmailData) -> Dict:
        """Extract structural features from email."""
        body = email.body

        # Body length
        body_length = len(body)

        # Check for greeting
        has_greeting = any(p.search(body) for p in self.GREETING_PATTERNS)

        # Check for signature
        has_signature = any(p.search(body) for p in self.SIGNATURE_PATTERNS)

        # Check for disclaimer
        has_disclaimer = any(p.search(body) for p in self.DISCLAIMER_PATTERNS)

        # Count paragraphs (separated by blank lines)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        paragraph_count = len(paragraphs)

        # Assess formality
        body_lower = body.lower()
        formal_count = sum(1 for ind in self.FORMAL_INDICATORS if ind in body_lower)
        casual_count = sum(1 for ind in self.CASUAL_INDICATORS if ind in body_lower)

        if formal_count > casual_count + 1:
            formality = "formal"
        elif casual_count > formal_count + 1:
            formality = "casual"
        else:
            formality = "semi-formal"

        # Analyze sender structure
        sender_features = self._analyze_sender_structure(email.sender)

        return {
            "body_length": body_length,
            "has_greeting": has_greeting,
            "has_signature": has_signature,
            "has_disclaimer": has_disclaimer,
            "paragraph_count": paragraph_count,
            "formality": formality,
            "has_url": email.has_url,
            "sender": sender_features,
        }

    def _analyze_sender_structure(self, sender: str) -> Dict:
        """Analyze sender address structure."""
        features = {
            "is_noreply": False,
            "has_department": False,
            "domain_type": "unknown",
        }

        # Check for noreply pattern
        if re.search(r"no.?reply|donotreply", sender, re.IGNORECASE):
            features["is_noreply"] = True

        # Check for department indicators
        dept_patterns = [
            "support",
            "billing",
            "sales",
            "info",
            "contact",
            "admin",
            "help",
            "service",
            "team",
            "notifications",
        ]
        local_part = sender.split("@")[0] if "@" in sender else sender
        features["has_department"] = any(d in local_part for d in dept_patterns)

        # Determine domain type
        if ".gov" in sender:
            features["domain_type"] = "government"
        elif ".edu" in sender:
            features["domain_type"] = "education"
        elif any(x in sender for x in [".org", ".net", ".com"]):
            features["domain_type"] = "commercial"

        return features

    def _score_template_match(
        self, features: Dict, profile: DomainProfile
    ) -> Tuple[float, Dict]:
        """Score how well features match a domain template."""
        score = 0.0
        details = {}

        # Body length match
        min_len, max_len = profile.typical_body_length
        body_len = features["body_length"]

        if min_len <= body_len <= max_len:
            score += self.WEIGHTS["body_length"]
            details["body_length"] = "match"
        elif body_len < min_len * 0.5 or body_len > max_len * 2:
            details["body_length"] = "mismatch"
        else:
            score += self.WEIGHTS["body_length"] * 0.5
            details["body_length"] = "partial"

        # Greeting match
        if features["has_greeting"] == profile.has_greeting:
            score += self.WEIGHTS["greeting"]
            details["greeting"] = "match"
        else:
            details["greeting"] = "mismatch"

        # Signature match
        if features["has_signature"] == profile.has_signature:
            score += self.WEIGHTS["signature"]
            details["signature"] = "match"
        else:
            details["signature"] = "mismatch"

        # Disclaimer match
        if features["has_disclaimer"] == profile.has_disclaimer:
            score += self.WEIGHTS["disclaimer"]
            details["disclaimer"] = "match"
        elif profile.has_disclaimer and features["has_disclaimer"]:
            score += self.WEIGHTS["disclaimer"]
            details["disclaimer"] = "match"
        else:
            details["disclaimer"] = "mismatch"

        # URL expectation match
        if features["has_url"] == profile.url_expected:
            score += self.WEIGHTS["url_match"]
            details["url"] = "match"
        else:
            score += self.WEIGHTS["url_match"] * 0.3
            details["url"] = "partial"

        # Formality match
        if features["formality"] == profile.formality_level:
            score += self.WEIGHTS["formality"]
            details["formality"] = "match"
        elif (
            features["formality"] == "semi-formal"
            or profile.formality_level == "semi-formal"
        ):
            score += self.WEIGHTS["formality"] * 0.5
            details["formality"] = "partial"
        else:
            details["formality"] = "mismatch"

        # Paragraph count match
        min_para, max_para = profile.typical_paragraph_count
        para_count = features["paragraph_count"]

        if min_para <= para_count <= max_para:
            score += self.WEIGHTS["paragraph_count"]
            details["paragraphs"] = "match"
        elif para_count < min_para * 0.5 or para_count > max_para * 2:
            details["paragraphs"] = "mismatch"
        else:
            score += self.WEIGHTS["paragraph_count"] * 0.5
            details["paragraphs"] = "partial"

        # Sender structure bonuses
        sender_features = features["sender"]
        if sender_features["domain_type"] == profile.name:
            score += self.WEIGHTS["sender_structure"]
            details["sender"] = "domain_match"
        elif sender_features["is_noreply"] and profile.name in [
            "technology",
            "retail",
            "logistics",
        ]:
            score += self.WEIGHTS["sender_structure"] * 0.5
            details["sender"] = "noreply_match"
        else:
            details["sender"] = "no_match"

        return score, details


class EmailClassifier:
    """
    Main classifier combining both methods.

    Classification logic:
    - Run Method 1 (Keyword Taxonomy)
    - Run Method 2 (Structural Template)
    - Calculate weighted combined score
    - Assign domain with highest score if above threshold
    """

    WEIGHT_METHOD_1 = 0.6  # Keywords
    WEIGHT_METHOD_2 = 0.4  # Structure
    GLOBAL_THRESHOLD = 0.15

    def __init__(self, domains: Dict[str, DomainProfile] = None):
        self.domains = domains or DOMAINS
        self.method1 = KeywordTaxonomyClassifier(self.domains)
        self.method2 = StructuralTemplateClassifier(self.domains)

    def classify(self, email: EmailData) -> Tuple[str, Dict]:
        """
        Classify email using dual-method validation with weighted scoring.

        Returns:
            Tuple of (domain_name or 'unsure', classification_details)
        """
        result1 = self.method1.classify(email)
        result2 = self.method2.classify(email)

        # Initialize details
        details = {
            "method1": {
                "domain": result1.domain,
                "confidence": result1.confidence,
                "scores": result1.scores,
            },
            "method2": {
                "domain": result2.domain,
                "confidence": result2.confidence,
                "scores": result2.scores,
            },
            "method_weights": {
                "method1": self.WEIGHT_METHOD_1,
                "method2": self.WEIGHT_METHOD_2,
            },
        }

        # Calculate combined scores
        combined_scores = {}
        all_domains = set(result1.scores.keys()) | set(result2.scores.keys())

        for domain in all_domains:
            score1 = result1.scores.get(domain, 0.0)
            score2 = result2.scores.get(domain, 0.0)

            combined_score = (score1 * self.WEIGHT_METHOD_1) + (
                score2 * self.WEIGHT_METHOD_2
            )
            combined_scores[domain] = combined_score

        details["combined_scores"] = combined_scores

        # Find best match
        if combined_scores:
            best_domain = max(combined_scores, key=combined_scores.get)
            best_score = combined_scores[best_domain]

            details["final_confidence"] = best_score

            if best_score >= self.GLOBAL_THRESHOLD:
                final_domain = best_domain
            else:
                final_domain = "unsure"
                details["reason"] = "below_threshold"
        else:
            final_domain = "unsure"
            details["reason"] = "no_scores"

        return final_domain, details

    def classify_dict(self, email_dict: Dict) -> Tuple[str, Dict]:
        """Classify email from dictionary input."""
        email = EmailData.from_dict(email_dict)
        return self.classify(email)
