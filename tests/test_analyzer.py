"""Tests for the DatasetAnalyzer module."""

import csv
import tempfile
from pathlib import Path

import pytest

from email_classifier.analyzer import AnalysisResult, DatasetAnalyzer


@pytest.fixture
def sample_csv_file():
    """Create a temporary CSV file with sample email data."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "sender",
                "receiver",
                "subject",
                "body",
                "label",
                "has_url",
            ],
        )
        writer.writeheader()

        # Add sample emails
        emails = [
            {
                "sender": "user1@gmail.com",
                "receiver": "dest1@company.com",
                "subject": "Test email 1",
                "body": "This is the body of test email 1. " * 10,
                "label": "spam",
                "has_url": "true",
            },
            {
                "sender": "user2@gmail.com",
                "receiver": "dest2@company.com",
                "subject": "Test email 2",
                "body": "Short body",
                "label": "ham",
                "has_url": "false",
            },
            {
                "sender": "user3@yahoo.com",
                "receiver": "dest3@company.com",
                "subject": "Test email 3",
                "body": "Medium length body content here. " * 5,
                "label": "spam",
                "has_url": "true",
            },
            {
                "sender": "user4@outlook.com",
                "receiver": "dest4@company.com",
                "subject": "",
                "body": "",
                "label": "ham",
                "has_url": "false",
            },
            {
                "sender": "invalid-email",
                "receiver": "also-invalid",
                "subject": "Invalid sender test",
                "body": "This has invalid sender format",
                "label": "unknown",
                "has_url": "false",
            },
        ]

        for email in emails:
            writer.writerow(email)

        return Path(f.name)


@pytest.fixture
def empty_csv_file():
    """Create an empty CSV file with just headers."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["sender", "receiver", "subject", "body", "label"],
        )
        writer.writeheader()
        return Path(f.name)


class TestDatasetAnalyzer:
    """Test suite for DatasetAnalyzer class."""

    def test_analyze_returns_analysis_result(self, sample_csv_file):
        """Test that analyze returns an AnalysisResult object."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert isinstance(result, AnalysisResult)

    def test_file_metadata(self, sample_csv_file):
        """Test that file metadata is correctly populated."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert result.file_path == str(sample_csv_file)
        assert result.file_size_bytes > 0
        assert result.total_rows == 5

    def test_label_distribution(self, sample_csv_file):
        """Test label distribution is correctly calculated."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert "spam" in result.label_counts
        assert "ham" in result.label_counts
        assert "unknown" in result.label_counts
        assert result.label_counts["spam"] == 2
        assert result.label_counts["ham"] == 2
        assert result.label_counts["unknown"] == 1

    def test_body_length_statistics(self, sample_csv_file):
        """Test body length statistics are calculated."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert result.body_length_min >= 0
        assert result.body_length_max >= result.body_length_min
        assert result.body_length_mean >= 0
        assert result.body_length_median >= 0

    def test_body_length_buckets(self, sample_csv_file):
        """Test body length buckets are populated."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert "0-100" in result.body_length_buckets
        assert "100-500" in result.body_length_buckets
        assert "500-1000" in result.body_length_buckets

        # Total bucket counts should equal total rows
        total_bucket = sum(result.body_length_buckets.values())
        assert total_bucket == result.total_rows

    def test_sender_domain_extraction(self, sample_csv_file):
        """Test sender domain extraction and counting."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert "gmail.com" in result.sender_domain_counts
        assert result.sender_domain_counts["gmail.com"] == 2
        assert "yahoo.com" in result.sender_domain_counts
        assert "outlook.com" in result.sender_domain_counts
        assert result.total_unique_domains >= 3

    def test_url_presence(self, sample_csv_file):
        """Test URL presence detection."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert result.url_count == 2
        assert result.url_percentage == pytest.approx(40.0, rel=0.1)

    def test_data_quality_empty_fields(self, sample_csv_file):
        """Test detection of empty fields."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        # One email has empty subject and body
        assert result.empty_subject_count == 1
        assert result.empty_body_count == 1

    def test_data_quality_invalid_format(self, sample_csv_file):
        """Test detection of invalid email format."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        # One email has invalid sender format
        assert result.invalid_sender_format_count == 1
        assert result.invalid_receiver_format_count == 1

    def test_columns_detected(self, sample_csv_file):
        """Test that CSV columns are correctly detected."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        assert "sender" in result.columns
        assert "receiver" in result.columns
        assert "subject" in result.columns
        assert "body" in result.columns
        assert "label" in result.columns
        assert result.has_label_column is True

    def test_empty_file(self, empty_csv_file):
        """Test handling of empty CSV file."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(empty_csv_file)

        assert result.total_rows == 0
        assert result.label_counts == {}
        assert result.body_length_min == 0
        assert result.body_length_max == 0

    def test_to_dict(self, sample_csv_file):
        """Test conversion to dictionary."""
        analyzer = DatasetAnalyzer()
        result = analyzer.analyze(sample_csv_file)

        result_dict = result.to_dict()

        assert "file" in result_dict
        assert "labels" in result_dict
        assert "body_length" in result_dict
        assert "sender_domains" in result_dict
        assert "urls" in result_dict
        assert "data_quality" in result_dict

        # Check nested structure
        assert "path" in result_dict["file"]
        assert "size_bytes" in result_dict["file"]
        assert "total_rows" in result_dict["file"]

    def test_progress_callback(self, sample_csv_file):
        """Test that progress callback is called."""
        analyzer = DatasetAnalyzer()
        progress_calls = []

        def callback(current, total, status):
            progress_calls.append((current, total, status))

        result = analyzer.analyze(sample_csv_file, progress_callback=callback)

        # Should have at least some progress calls
        assert len(progress_calls) > 0
        # Last call should indicate completion
        assert "complete" in progress_calls[-1][2].lower()


class TestAnalysisResult:
    """Test suite for AnalysisResult class."""

    def test_default_values(self):
        """Test default values of AnalysisResult."""
        result = AnalysisResult()

        assert result.file_path == ""
        assert result.file_size_bytes == 0
        assert result.total_rows == 0
        assert result.label_counts == {}
        assert result.body_length_min == 0
        assert result.body_length_max == 0

    def test_format_size_bytes(self):
        """Test size formatting for bytes."""
        result = AnalysisResult()
        assert result._format_size(500) == "500.0 B"

    def test_format_size_kilobytes(self):
        """Test size formatting for kilobytes."""
        result = AnalysisResult()
        assert result._format_size(2048) == "2.0 KB"

    def test_format_size_megabytes(self):
        """Test size formatting for megabytes."""
        result = AnalysisResult()
        assert result._format_size(1048576) == "1.0 MB"

    def test_format_size_gigabytes(self):
        """Test size formatting for gigabytes."""
        result = AnalysisResult()
        assert result._format_size(1073741824) == "1.0 GB"
