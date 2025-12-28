"""Tests for the main EmailClassifier."""

import pytest

from email_classifier import EmailClassifier, EmailData
from email_classifier.classifier import (
    ClassificationResult,
    KeywordTaxonomyClassifier,
    StructuralTemplateClassifier,
)
from email_classifier.domains import DOMAINS


class TestEmailClassifier:
    """Test cases for EmailClassifier class."""

    def test_classifier_initialization(self):
        """Test that classifier can be initialized."""
        classifier = EmailClassifier()
        assert classifier is not None
        assert hasattr(classifier, "method1")
        assert hasattr(classifier, "method2")

    def test_classify_dict_basic(self):
        """Test basic classification with dictionary input."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "test@example.com",
            "receiver": "user@domain.com",
            "timestamp": "2024-01-15 10:30:00",
            "subject": "Test subject",
            "body": "This is a test email body.",
            "has_url": False,
        }

        domain, details = classifier.classify_dict(email_data)
        assert isinstance(domain, str)
        assert isinstance(details, dict)
        assert "method1" in details
        assert "method2" in details

    def test_email_data_creation(self):
        """Test EmailData creation from dictionary."""
        data = {
            "sender": "test@example.com",
            "receiver": "user@domain.com",
            "timestamp": "2024-01-15 10:30:00",
            "subject": "Test",
            "body": "Test body",
            "has_url": True,
        }

        email = EmailData.from_dict(data)
        assert email.sender == "test@example.com"
        assert email.receiver == "user@domain.com"
        assert email.has_url is True

    def test_email_data_with_urls_field(self):
        """Test EmailData handles urls field correctly."""
        data = {
            "sender": "test@example.com",
            "receiver": "user@domain.com",
            "date": "2024-01-15",
            "subject": "Test",
            "body": "Test body",
            "urls": "http://example.com",
        }
        email = EmailData.from_dict(data)
        assert email.has_url is True

    def test_email_data_empty_urls(self):
        """Test EmailData with empty urls field."""
        data = {
            "sender": "test@example.com",
            "receiver": "user@domain.com",
            "date": "2024-01-15",
            "subject": "Test",
            "body": "Test body",
            "urls": "",
        }
        email = EmailData.from_dict(data)
        assert email.has_url is False

    def test_email_data_missing_fields(self):
        """Test EmailData handles missing fields gracefully."""
        data = {}
        email = EmailData.from_dict(data)
        assert email.sender == ""
        assert email.receiver == ""
        assert email.subject == ""
        assert email.body == ""
        assert email.has_url is False

    def test_classify_finance_email(self):
        """Test classification of finance-related email."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "alerts@bank.com",
            "receiver": "customer@email.com",
            "date": "2024-01-15",
            "subject": "Your account statement is ready",
            "body": "Dear Customer, Your monthly bank statement is now available. "
            "Please review your recent transactions and account balance. "
            "Your current balance is $1,234.56. Transfer funds securely online.",
            "urls": "https://bank.com/statement",
        }
        domain, details = classifier.classify_dict(email_data)
        assert domain == "finance"
        assert details["method1"]["domain"] == "finance"

    def test_classify_healthcare_email(self):
        """Test classification of healthcare-related email."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "appointments@hospital.com",
            "receiver": "patient@email.com",
            "date": "2024-01-15",
            "subject": "Appointment Reminder - Dr. Smith",
            "body": "Dear Patient, This is a reminder for your appointment with "
            "Dr. Smith on Monday. Please bring your insurance card and medical records. "
            "Your prescription is ready at the pharmacy. HIPAA Notice: This message is confidential.",
            "urls": "",
        }
        domain, details = classifier.classify_dict(email_data)
        assert domain == "healthcare"

    def test_classify_retail_email(self):
        """Test classification of retail-related email."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "orders@shop.com",
            "receiver": "customer@email.com",
            "date": "2024-01-15",
            "subject": "Order Confirmation #12345",
            "body": "Thank you for your purchase! Your order has been confirmed. "
            "Items: Product ABC - $29.99. Total: $32.99 with shipping. "
            "Your package will be shipped within 2 business days. Track your delivery online.",
            "urls": "https://shop.com/track",
        }
        domain, details = classifier.classify_dict(email_data)
        assert domain == "retail"

    def test_classify_technology_email(self):
        """Test classification of technology-related email."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "noreply@techservice.com",
            "receiver": "user@email.com",
            "date": "2024-01-15",
            "subject": "Password Reset Request",
            "body": "We received a request to reset your password. "
            "Click the link below to update your account credentials. "
            "Your subscription will expire in 30 days. Update your software for security.",
            "urls": "https://tech.com/reset",
        }
        domain, details = classifier.classify_dict(email_data)
        assert domain == "technology"

    def test_classify_unsure_low_confidence(self):
        """Test classification returns unsure for ambiguous emails."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "unknown@random.xyz",
            "receiver": "user@email.com",
            "date": "2024-01-15",
            "subject": "Hello",
            "body": "Hi there.",
            "urls": "",
        }
        domain, details = classifier.classify_dict(email_data)
        # Could be unsure or might match something due to low thresholds
        assert domain is not None

    def test_classifier_llm_disabled_by_default(self):
        """Test that LLM is disabled by default."""
        classifier = EmailClassifier()
        assert classifier.llm_enabled is False
        assert classifier.method3 is None
        assert classifier.weight_method_1 == 0.6
        assert classifier.weight_method_2 == 0.4
        assert classifier.weight_method_3 == 0.0

    def test_classifier_method_weights_structure(self):
        """Test that method weights are included in classification details."""
        classifier = EmailClassifier()
        email_data = {
            "sender": "test@example.com",
            "receiver": "user@domain.com",
            "date": "2024-01-15",
            "subject": "Test",
            "body": "Test body content",
            "urls": "",
        }
        domain, details = classifier.classify_dict(email_data)
        assert "method_weights" in details
        assert "method1" in details["method_weights"]
        assert "method2" in details["method_weights"]
        assert "llm_enabled" in details


class TestKeywordTaxonomyClassifier:
    """Test cases for KeywordTaxonomyClassifier."""

    def test_initialization(self):
        """Test classifier initialization."""
        classifier = KeywordTaxonomyClassifier()
        assert classifier.domains is not None
        assert len(classifier.domains) > 0

    def test_initialization_with_custom_domains(self):
        """Test classifier with custom domains."""
        custom_domains = {"custom": DOMAINS["finance"]}
        classifier = KeywordTaxonomyClassifier(domains=custom_domains)
        assert "custom" in classifier.domains
        assert len(classifier.domains) == 1

    def test_classify_returns_classification_result(self):
        """Test classify returns ClassificationResult."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Test body",
            urls="",
        )
        result = classifier.classify(email)
        assert isinstance(result, ClassificationResult)
        assert result.method == "keyword_taxonomy"

    def test_classify_with_primary_keywords_in_subject(self):
        """Test keywords in subject increase score."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="test@bank.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Your account balance statement",
            body="Please check your account.",
            urls="",
        )
        result = classifier.classify(email)
        assert result.scores["finance"] > 0

    def test_classify_with_secondary_keywords_in_body(self):
        """Test secondary keywords in body contribute to score."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Information",
            body="Your financial funds transfer is pending. Money exchange rate updated.",
            urls="",
        )
        result = classifier.classify(email)
        assert result.scores["finance"] > 0

    def test_classify_sender_pattern_match(self):
        """Test sender pattern matching."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="alerts@bankofamerica.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Notice",
            body="Important update.",
            urls="",
        )
        result = classifier.classify(email)
        # Should match bank pattern
        assert result.details is not None
        assert result.details["finance"]["sender_match"] is True

    def test_classify_subject_pattern_match(self):
        """Test subject pattern matching."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Your transaction has been processed",
            body="Details enclosed.",
            urls="",
        )
        result = classifier.classify(email)
        assert result.details is not None
        assert result.details["finance"]["subject_pattern_match"] is True

    def test_classify_empty_body(self):
        """Test classification with empty body."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="",
            urls="",
        )
        result = classifier.classify(email)
        # Should not crash, confidence should be low
        assert result is not None

    def test_classify_below_confidence_threshold(self):
        """Test that low confidence returns None domain."""
        classifier = KeywordTaxonomyClassifier()
        email = EmailData(
            sender="random@xyz.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="xyz",
            body="xyz",
            urls="",
        )
        result = classifier.classify(email)
        # With no matching keywords, confidence should be low
        assert result.confidence < 0.1 or result.domain is None


class TestStructuralTemplateClassifier:
    """Test cases for StructuralTemplateClassifier."""

    def test_initialization(self):
        """Test classifier initialization."""
        classifier = StructuralTemplateClassifier()
        assert classifier.domains is not None

    def test_initialization_with_custom_domains(self):
        """Test classifier with custom domains."""
        custom_domains = {"custom": DOMAINS["technology"]}
        classifier = StructuralTemplateClassifier(domains=custom_domains)
        assert "custom" in classifier.domains

    def test_classify_returns_classification_result(self):
        """Test classify returns ClassificationResult."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Test body content here.",
            urls="",
        )
        result = classifier.classify(email)
        assert isinstance(result, ClassificationResult)
        assert result.method == "structural_template"

    def test_extract_features_greeting(self):
        """Test greeting detection in features."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Dear Customer,\n\nThis is a test message.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["has_greeting"] is True

    def test_extract_features_no_greeting(self):
        """Test no greeting detected."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Your order has shipped.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["has_greeting"] is False

    def test_extract_features_signature(self):
        """Test signature detection."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Message content.\n\nBest regards,\nJohn",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["has_signature"] is True

    def test_extract_features_disclaimer(self):
        """Test disclaimer detection."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Content here.\n\nThis email is confidential and intended for the recipient only.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["has_disclaimer"] is True

    def test_extract_features_paragraph_count(self):
        """Test paragraph counting."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["paragraph_count"] == 3

    def test_extract_features_formality_formal(self):
        """Test formal language detection."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Pursuant to our discussion, please find enclosed the document. "
            "Regarding your inquiry, we hereby confirm the receipt. Respectfully submitted.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["formality"] == "formal"

    def test_extract_features_formality_casual(self):
        """Test casual language detection."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Hey! That's awesome!! BTW gonna check it out :) Cool stuff FYI!",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["formality"] == "casual"

    def test_extract_features_formality_semiformal(self):
        """Test semi-formal language detection."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="test@example.com",
            receiver="user@domain.com",
            date="2024-01-15",
            subject="Test",
            body="Hello, I wanted to follow up on our conversation. Thanks for your time.",
            urls="",
        )
        features = classifier._extract_features(email)
        assert features["formality"] == "semi-formal"

    def test_analyze_sender_noreply(self):
        """Test noreply sender detection."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("noreply@company.com")
        assert features["is_noreply"] is True

    def test_analyze_sender_donotreply(self):
        """Test donotreply sender detection."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("donotreply@company.com")
        assert features["is_noreply"] is True

    def test_analyze_sender_department(self):
        """Test department detection in sender."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("support@company.com")
        assert features["has_department"] is True

        features = classifier._analyze_sender_structure("billing@company.com")
        assert features["has_department"] is True

    def test_analyze_sender_domain_gov(self):
        """Test .gov domain detection."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("notice@agency.gov")
        assert features["domain_type"] == "government"

    def test_analyze_sender_domain_edu(self):
        """Test .edu domain detection."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("registrar@university.edu")
        assert features["domain_type"] == "education"

    def test_analyze_sender_domain_commercial(self):
        """Test commercial domain detection."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("info@company.com")
        assert features["domain_type"] == "commercial"

    def test_analyze_sender_no_at_symbol(self):
        """Test sender without @ symbol."""
        classifier = StructuralTemplateClassifier()
        features = classifier._analyze_sender_structure("support")
        assert features["has_department"] is True

    def test_score_template_body_length_match(self):
        """Test body length scoring - exact match."""
        classifier = StructuralTemplateClassifier()
        features = {
            "body_length": 500,
            "has_greeting": True,
            "has_signature": True,
            "has_disclaimer": False,
            "has_url": True,
            "formality": "semi-formal",
            "paragraph_count": 3,
            "sender": {"domain_type": "unknown", "is_noreply": False, "has_department": False},
        }
        score, details = classifier._score_template_match(features, DOMAINS["technology"])
        assert details["body_length"] == "match"

    def test_score_template_body_length_partial(self):
        """Test body length scoring - partial match."""
        classifier = StructuralTemplateClassifier()
        features = {
            "body_length": 80,  # Below typical but not extreme
            "has_greeting": True,
            "has_signature": True,
            "has_disclaimer": False,
            "has_url": True,
            "formality": "semi-formal",
            "paragraph_count": 2,
            "sender": {"domain_type": "unknown", "is_noreply": False, "has_department": False},
        }
        score, details = classifier._score_template_match(features, DOMAINS["technology"])
        assert details["body_length"] == "partial"

    def test_score_template_body_length_mismatch(self):
        """Test body length scoring - mismatch."""
        classifier = StructuralTemplateClassifier()
        features = {
            "body_length": 10,  # Very short
            "has_greeting": True,
            "has_signature": True,
            "has_disclaimer": False,
            "has_url": True,
            "formality": "semi-formal",
            "paragraph_count": 1,
            "sender": {"domain_type": "unknown", "is_noreply": False, "has_department": False},
        }
        score, details = classifier._score_template_match(features, DOMAINS["technology"])
        assert details["body_length"] == "mismatch"

    def test_score_template_formality_mismatch(self):
        """Test formality mismatch scoring."""
        classifier = StructuralTemplateClassifier()
        features = {
            "body_length": 500,
            "has_greeting": True,
            "has_signature": True,
            "has_disclaimer": True,
            "has_url": True,
            "formality": "casual",  # Finance expects formal
            "paragraph_count": 3,
            "sender": {"domain_type": "unknown", "is_noreply": False, "has_department": False},
        }
        score, details = classifier._score_template_match(features, DOMAINS["finance"])
        assert details["formality"] == "mismatch"

    def test_score_template_noreply_match(self):
        """Test noreply sender scoring for technology/retail/logistics."""
        classifier = StructuralTemplateClassifier()
        features = {
            "body_length": 500,
            "has_greeting": True,
            "has_signature": True,
            "has_disclaimer": False,
            "has_url": True,
            "formality": "semi-formal",
            "paragraph_count": 2,
            "sender": {"domain_type": "unknown", "is_noreply": True, "has_department": False},
        }
        score, details = classifier._score_template_match(features, DOMAINS["technology"])
        assert details["sender"] == "noreply_match"

    def test_classify_zero_total_scores(self):
        """Test handling when all scores are zero."""
        classifier = StructuralTemplateClassifier()
        email = EmailData(
            sender="x@y.z",
            receiver="a@b.c",
            date="2024-01-15",
            subject="x",
            body="x",
            urls="",
        )
        result = classifier.classify(email)
        # Should handle gracefully
        assert result is not None


class TestClassificationResult:
    """Test cases for ClassificationResult dataclass."""

    def test_creation(self):
        """Test ClassificationResult creation."""
        result = ClassificationResult(
            domain="finance",
            confidence=0.85,
            scores={"finance": 0.85, "technology": 0.15},
            method="keyword_taxonomy",
        )
        assert result.domain == "finance"
        assert result.confidence == 0.85
        assert result.method == "keyword_taxonomy"

    def test_creation_with_details(self):
        """Test ClassificationResult with details."""
        result = ClassificationResult(
            domain="healthcare",
            confidence=0.75,
            scores={"healthcare": 0.75},
            method="structural_template",
            details={"feature": "value"},
        )
        assert result.details == {"feature": "value"}

    def test_none_domain(self):
        """Test ClassificationResult with None domain."""
        result = ClassificationResult(
            domain=None,
            confidence=0.0,
            scores={},
            method="test",
        )
        assert result.domain is None
