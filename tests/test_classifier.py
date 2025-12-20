"""Tests for the main EmailClassifier."""

import pytest
from email_classifier import EmailClassifier, EmailData


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
