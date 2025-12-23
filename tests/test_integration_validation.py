"""
Integration tests for email validation and output standardization.
"""

import csv
import tempfile
from pathlib import Path

import pytest

from email_classifier.classifier import EmailClassifier
from email_classifier.processor import StreamingProcessor, OutputManager


class TestIntegrationValidation:
    """Integration tests for validation in the processing pipeline."""

    def create_test_csv(self, data: list, fieldnames: list, filepath: Path):
        """Helper to create test CSV files."""
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def test_invalid_emails_skipped_and_logged(self):
        """Test that invalid emails are skipped and logged to invalid_emails.csv."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            # Create test data with mix of valid and invalid emails
            data = [
                {
                    "sender": "valid@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "Valid Email",
                    "body": "This is a valid email body.",
                    "timestamp": "2024-01-15",
                    "has_url": "true",
                },
                {
                    "sender": "invalid-sender",  # Invalid sender
                    "receiver": "recipient@example.com",
                    "subject": "Invalid Sender",
                    "body": "This email has invalid sender.",
                    "timestamp": "2024-01-15",
                    "has_url": "false",
                },
                {
                    "sender": "sender@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "",  # Empty subject
                    "body": "This email has empty subject.",
                    "timestamp": "2024-01-15",
                    "has_url": "true",
                },
                {
                    "sender": "another@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "Another Valid Email",
                    "body": "This is another valid email.",
                    "timestamp": "2024-01-16",
                    "has_url": "false",
                },
            ]

            fieldnames = ["sender", "receiver", "subject", "body", "timestamp", "has_url"]
            self.create_test_csv(data, fieldnames, input_path)

            # Process
            processor = StreamingProcessor()
            stats = processor.process(input_path, output_dir)

            # Verify stats
            assert stats.total_processed == 2  # Only valid emails processed
            assert stats.validation_stats.total_invalid == 2  # 2 invalid emails

            # Verify invalid_emails.csv was created
            invalid_path = output_dir / "invalid_emails.csv"
            assert invalid_path.exists()

            with open(invalid_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                invalid_rows = list(reader)

            assert len(invalid_rows) == 2

            # Check error reasons
            errors = [row["validation_errors"] for row in invalid_rows]
            assert any("invalid_sender_format" in e for e in errors)
            assert any("empty_subject" in e for e in errors)

    def test_strict_validation_fails_on_invalid(self):
        """Test that strict validation mode fails on first invalid email."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            data = [
                {
                    "sender": "invalid-sender",  # Invalid
                    "receiver": "recipient@example.com",
                    "subject": "Test",
                    "body": "Test body",
                    "timestamp": "2024-01-15",
                    "has_url": "false",
                },
            ]

            fieldnames = ["sender", "receiver", "subject", "body", "timestamp", "has_url"]
            self.create_test_csv(data, fieldnames, input_path)

            # Process with strict validation
            processor = StreamingProcessor(strict_validation=True)

            with pytest.raises(ValueError) as excinfo:
                processor.process(input_path, output_dir)

            assert "Validation failed" in str(excinfo.value)


class TestIntegrationOutputStandardization:
    """Integration tests for output column standardization."""

    def create_test_csv(self, data: list, fieldnames: list, filepath: Path):
        """Helper to create test CSV files."""
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def test_output_columns_in_standard_order(self):
        """Test that output CSV files have columns in standard order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            # Create test data with columns in non-standard order
            data = [
                {
                    "body": "Test email body content for classification.",
                    "timestamp": "2024-01-15",
                    "subject": "Financial Report",
                    "has_url": "true",
                    "receiver": "recipient@example.com",
                    "sender": "finance@bank.com",
                },
            ]

            # Input columns in non-standard order
            fieldnames = ["body", "timestamp", "subject", "has_url", "receiver", "sender"]
            self.create_test_csv(data, fieldnames, input_path)

            # Process
            processor = StreamingProcessor()
            processor.process(input_path, output_dir)

            # Find output files
            output_files = list(output_dir.glob("email_*.csv"))
            assert len(output_files) > 0

            # Check column order in output
            with open(output_files[0], "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                output_fieldnames = reader.fieldnames

            # Standard columns should be first
            expected_start = ["sender", "receiver", "date", "subject", "body", "urls", "label"]
            for i, col in enumerate(expected_start):
                assert output_fieldnames[i] == col, f"Column {i} should be {col}, got {output_fieldnames[i]}"

    def test_timestamp_mapped_to_date(self):
        """Test that 'timestamp' column is mapped to 'date'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            data = [
                {
                    "sender": "sender@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "Test Email",
                    "body": "Test email body.",
                    "timestamp": "2024-01-15 10:30:00",
                    "has_url": "false",
                },
            ]

            fieldnames = ["sender", "receiver", "subject", "body", "timestamp", "has_url"]
            self.create_test_csv(data, fieldnames, input_path)

            processor = StreamingProcessor()
            processor.process(input_path, output_dir)

            output_files = list(output_dir.glob("email_*.csv"))
            with open(output_files[0], "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            # Check that 'date' column exists and has the timestamp value
            assert "date" in reader.fieldnames
            assert "timestamp" not in reader.fieldnames
            assert rows[0]["date"] == "2024-01-15 10:30:00"

    def test_has_url_mapped_to_urls(self):
        """Test that 'has_url' column is mapped to 'urls'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            data = [
                {
                    "sender": "sender@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "Test Email with URL",
                    "body": "Test email body with a link.",
                    "timestamp": "2024-01-15",
                    "has_url": "true",
                },
                {
                    "sender": "sender2@example.com",
                    "receiver": "recipient2@example.com",
                    "subject": "Test Email without URL",
                    "body": "Test email body without links.",
                    "timestamp": "2024-01-16",
                    "has_url": "false",
                },
            ]

            fieldnames = ["sender", "receiver", "subject", "body", "timestamp", "has_url"]
            self.create_test_csv(data, fieldnames, input_path)

            processor = StreamingProcessor()
            processor.process(input_path, output_dir)

            output_files = list(output_dir.glob("email_*.csv"))

            all_rows = []
            for f in output_files:
                with open(f, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    all_rows.extend(list(reader))

            # Check that 'urls' column exists and has converted values
            assert any("urls" in row for row in all_rows)
            urls_values = [row.get("urls", "") for row in all_rows]
            assert "true" in urls_values  # has_url=true should become urls="true"

    def test_validation_stats_in_report(self):
        """Test that validation statistics appear in processing stats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"

            data = [
                {
                    "sender": "valid@example.com",
                    "receiver": "recipient@example.com",
                    "subject": "Valid",
                    "body": "Valid body",
                    "timestamp": "2024-01-15",
                    "has_url": "false",
                },
                {
                    "sender": "invalid",
                    "receiver": "recipient@example.com",
                    "subject": "",
                    "body": "",
                    "timestamp": "2024-01-15",
                    "has_url": "false",
                },
            ]

            fieldnames = ["sender", "receiver", "subject", "body", "timestamp", "has_url"]
            self.create_test_csv(data, fieldnames, input_path)

            processor = StreamingProcessor()
            stats = processor.process(input_path, output_dir)

            # Convert to dict and check validation section
            stats_dict = stats.to_dict()
            assert "validation" in stats_dict
            assert stats_dict["validation"]["total_invalid"] == 1
            assert stats_dict["validation"]["invalid_sender_format"] == 1
            assert stats_dict["validation"]["invalid_empty_subject"] == 1
            assert stats_dict["validation"]["invalid_empty_body"] == 1


class TestOutputManagerStandardColumns:
    """Tests for OutputManager standard column ordering."""

    def test_build_fieldnames_standard_order(self):
        """Test that _build_fieldnames produces correct column order."""
        input_fieldnames = ["body", "timestamp", "subject", "sender", "receiver", "extra_col"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_manager = OutputManager(Path(tmpdir), input_fieldnames, include_details=False)

            fieldnames = output_manager.fieldnames

            # Verify standard columns come first
            expected_standard = ["sender", "receiver", "date", "subject", "body", "urls", "label"]
            for i, col in enumerate(expected_standard):
                assert fieldnames[i] == col

            # Verify classification columns follow
            assert "classified_domain" in fieldnames
            assert "method1_domain" in fieldnames
            assert "method2_domain" in fieldnames

            # Verify extra columns are included
            assert "extra_col" in fieldnames

    def test_build_fieldnames_with_details(self):
        """Test that detail columns are included when requested."""
        input_fieldnames = ["sender", "receiver", "subject", "body"]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_manager = OutputManager(Path(tmpdir), input_fieldnames, include_details=True)

            fieldnames = output_manager.fieldnames

            # Verify detail columns are included
            assert "method1_confidence" in fieldnames
            assert "method2_confidence" in fieldnames
            assert "agreement" in fieldnames
