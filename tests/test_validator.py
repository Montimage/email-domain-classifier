"""
Unit tests for email validation functionality.
"""

import csv
import tempfile
from pathlib import Path

import pytest

from email_classifier.validator import (
    EmailValidator,
    InvalidEmailWriter,
    ValidationResult,
    ValidationStats,
)


class TestEmailValidator:
    """Tests for EmailValidator class."""

    @pytest.fixture
    def validator(self):
        """Create EmailValidator instance."""
        return EmailValidator()

    # Email format validation tests
    def test_valid_email_formats(self, validator):
        """Test validation of various valid email formats."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example.co.uk",
            "USER@EXAMPLE.COM",
            "test@subdomain.example.org",
            "a@b.co",
            "user_name@example.com",
            "user-name@example.com",
            "user%name@example.com",
        ]
        for email in valid_emails:
            assert validator.validate_email_format(email), f"Should be valid: {email}"

    def test_valid_email_with_display_name(self, validator):
        """Test validation of emails in 'Display Name <email>' format."""
        valid_emails = [
            "Young Esposito <Young@iworld.de>",
            "John Doe <john@example.com>",
            '"John Doe" <john@example.com>',
            "Jane Smith <jane.smith@company.co.uk>",
            "Support Team <support@help.org>",
            "<simple@email.com>",
            "Name With Spaces <user@domain.com>",
            "First Last <first.last+tag@example.com>",
        ]
        for email in valid_emails:
            assert validator.validate_email_format(email), f"Should be valid: {email}"

    def test_invalid_email_formats(self, validator):
        """Test validation of various invalid email formats."""
        invalid_emails = [
            "not-an-email",
            "missing-at-sign.com",
            "@no-local-part.com",
            "no-domain@",
            "spaces in@email.com",
            "user@.com",
            "user@example.",
            "",
            "   ",
        ]
        for email in invalid_emails:
            assert not validator.validate_email_format(email), f"Should be invalid: {email}"

    def test_none_email_returns_false(self, validator):
        """Test that None email returns False (not valid)."""
        # The validator should handle None gracefully by returning False
        # since str(None) = "None" which is not a valid email
        result = validator.validate_email_format("None")
        assert not result

    def test_email_with_whitespace_trimmed(self, validator):
        """Test that emails with surrounding whitespace are handled."""
        assert validator.validate_email_format("  user@example.com  ")
        assert validator.validate_email_format("\tuser@example.com\n")

    # Full email record validation tests
    def test_valid_email_record(self, validator):
        """Test validation of a complete valid email record."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "receiver@example.com",
            "subject": "Test Subject",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_empty_sender_fails(self, validator):
        """Test that empty sender fails validation."""
        email_dict = {
            "sender": "",
            "receiver": "receiver@example.com",
            "subject": "Test Subject",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_sender" in result.errors

    def test_empty_receiver_fails(self, validator):
        """Test that empty receiver fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "",
            "subject": "Test Subject",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_receiver" in result.errors

    def test_invalid_sender_format_fails(self, validator):
        """Test that invalid sender format fails validation."""
        email_dict = {
            "sender": "not-valid-email",
            "receiver": "receiver@example.com",
            "subject": "Test Subject",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "invalid_sender_format" in result.errors

    def test_invalid_receiver_format_fails(self, validator):
        """Test that invalid receiver format fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "not-valid-email",
            "subject": "Test Subject",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "invalid_receiver_format" in result.errors

    def test_empty_subject_fails(self, validator):
        """Test that empty subject fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "receiver@example.com",
            "subject": "",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_subject" in result.errors

    def test_whitespace_only_subject_fails(self, validator):
        """Test that whitespace-only subject fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "receiver@example.com",
            "subject": "   \t\n  ",
            "body": "This is the email body.",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_subject" in result.errors

    def test_empty_body_fails(self, validator):
        """Test that empty body fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "receiver@example.com",
            "subject": "Test Subject",
            "body": "",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_body" in result.errors

    def test_whitespace_only_body_fails(self, validator):
        """Test that whitespace-only body fails validation."""
        email_dict = {
            "sender": "sender@example.com",
            "receiver": "receiver@example.com",
            "subject": "Test Subject",
            "body": "   \n\t   ",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_body" in result.errors

    def test_multiple_errors_collected(self, validator):
        """Test that multiple validation errors are collected."""
        email_dict = {
            "sender": "not-valid",
            "receiver": "",
            "subject": "",
            "body": "Valid body",
        }
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert len(result.errors) == 3
        assert "invalid_sender_format" in result.errors
        assert "empty_receiver" in result.errors
        assert "empty_subject" in result.errors

    def test_missing_fields_treated_as_empty(self, validator):
        """Test that missing fields are treated as empty."""
        email_dict = {}
        result = validator.validate(email_dict)
        assert not result.is_valid
        assert "empty_sender" in result.errors
        assert "empty_receiver" in result.errors
        assert "empty_subject" in result.errors
        assert "empty_body" in result.errors


class TestInvalidEmailWriter:
    """Tests for InvalidEmailWriter class."""

    def test_write_invalid_email(self):
        """Test writing invalid email to CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            fieldnames = ["sender", "receiver", "subject", "body"]

            writer = InvalidEmailWriter(output_dir, fieldnames)

            email_dict = {
                "sender": "bad-email",
                "receiver": "receiver@example.com",
                "subject": "Test",
                "body": "Body text",
            }
            errors = ["invalid_sender_format"]

            writer.write(email_dict, errors)
            writer.close()

            # Verify file was created
            csv_path = output_dir / "invalid_emails.csv"
            assert csv_path.exists()

            # Verify content
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == 1
            assert rows[0]["sender"] == "bad-email"
            assert rows[0]["validation_errors"] == "invalid_sender_format"

    def test_write_multiple_errors(self):
        """Test writing email with multiple validation errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            fieldnames = ["sender", "receiver", "subject", "body"]

            writer = InvalidEmailWriter(output_dir, fieldnames)

            email_dict = {
                "sender": "bad-email",
                "receiver": "",
                "subject": "",
                "body": "Body",
            }
            errors = ["invalid_sender_format", "empty_receiver", "empty_subject"]

            writer.write(email_dict, errors)
            writer.close()

            csv_path = output_dir / "invalid_emails.csv"
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert rows[0]["validation_errors"] == "invalid_sender_format|empty_receiver|empty_subject"

    def test_stats_tracking(self):
        """Test that validation statistics are tracked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            fieldnames = ["sender", "receiver", "subject", "body"]

            writer = InvalidEmailWriter(output_dir, fieldnames)

            # Write first invalid email
            writer.write(
                {"sender": "bad", "receiver": "r@e.com", "subject": "S", "body": "B"},
                ["invalid_sender_format"],
            )

            # Write second invalid email with multiple errors
            writer.write(
                {"sender": "s@e.com", "receiver": "", "subject": "", "body": ""},
                ["empty_receiver", "empty_subject", "empty_body"],
            )

            stats = writer.get_stats()
            writer.close()

            assert stats.total_invalid == 2
            assert stats.invalid_sender_format == 1
            assert stats.invalid_empty_receiver == 1
            assert stats.invalid_empty_subject == 1
            assert stats.invalid_empty_body == 1

    def test_context_manager(self):
        """Test using InvalidEmailWriter as context manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            fieldnames = ["sender", "receiver", "subject", "body"]

            with InvalidEmailWriter(output_dir, fieldnames) as writer:
                writer.write(
                    {"sender": "bad", "receiver": "r@e.com", "subject": "S", "body": "B"},
                    ["invalid_sender_format"],
                )

            # File should be closed automatically
            csv_path = output_dir / "invalid_emails.csv"
            assert csv_path.exists()


class TestValidationStats:
    """Tests for ValidationStats class."""

    def test_default_values(self):
        """Test that ValidationStats initializes with zeros."""
        stats = ValidationStats()
        assert stats.total_invalid == 0
        assert stats.invalid_sender_format == 0
        assert stats.invalid_receiver_format == 0
        assert stats.invalid_empty_sender == 0
        assert stats.invalid_empty_receiver == 0
        assert stats.invalid_empty_subject == 0
        assert stats.invalid_empty_body == 0

    def test_to_dict(self):
        """Test converting ValidationStats to dictionary."""
        stats = ValidationStats(
            total_invalid=5,
            invalid_sender_format=2,
            invalid_empty_subject=3,
        )
        result = stats.to_dict()

        assert result["total_invalid"] == 5
        assert result["invalid_sender_format"] == 2
        assert result["invalid_empty_subject"] == 3
        assert result["invalid_empty_body"] == 0
