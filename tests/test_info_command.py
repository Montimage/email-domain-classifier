"""Integration tests for the info command."""

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


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
                "subject": "Order confirmation",
                "body": "Thank you for your order. Your tracking number is 12345.",
                "label": "retail",
                "has_url": "true",
            },
            {
                "sender": "bank@example.com",
                "receiver": "dest2@company.com",
                "subject": "Account statement",
                "body": "Your monthly account statement is ready.",
                "label": "finance",
                "has_url": "false",
            },
            {
                "sender": "support@tech.com",
                "receiver": "dest3@company.com",
                "subject": "Password reset",
                "body": "Click here to reset your password.",
                "label": "technology",
                "has_url": "true",
            },
        ]

        for email in emails:
            writer.writerow(email)

        return Path(f.name)


class TestInfoCommand:
    """Integration tests for email-cli info command."""

    def test_info_command_basic(self, sample_csv_file):
        """Test basic info command execution."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "email_classifier.cli",
                "info",
                str(sample_csv_file),
            ],
            capture_output=True,
            text=True,
        )

        # Command should succeed
        assert result.returncode == 0

    def test_info_command_json_output(self, sample_csv_file):
        """Test info command with JSON output."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "email_classifier.cli",
                "info",
                str(sample_csv_file),
                "--json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Parse JSON output
        output = json.loads(result.stdout)

        # Check structure
        assert "file" in output
        assert "labels" in output
        assert "body_length" in output
        assert "sender_domains" in output
        assert "urls" in output
        assert "data_quality" in output

        # Check values
        assert output["file"]["total_rows"] == 3
        assert "retail" in output["labels"]["distribution"]
        assert "finance" in output["labels"]["distribution"]
        assert "technology" in output["labels"]["distribution"]

    def test_info_command_nonexistent_file(self):
        """Test info command with non-existent file."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "email_classifier.cli",
                "info",
                "nonexistent.csv",
                "--json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1

        output = json.loads(result.stdout)
        assert "error" in output
        assert "not found" in output["error"].lower()

    def test_info_command_non_csv_file(self):
        """Test info command with non-CSV file."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"This is not a CSV file")
            txt_file = Path(f.name)

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "email_classifier.cli",
                    "info",
                    str(txt_file),
                    "--json",
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 1

            output = json.loads(result.stdout)
            assert "error" in output
            assert "csv" in output["error"].lower()
        finally:
            txt_file.unlink()

    def test_info_command_quiet_mode(self, sample_csv_file):
        """Test info command with quiet mode."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "email_classifier.cli",
                "info",
                str(sample_csv_file),
                "--quiet",
                "--json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Should still output JSON
        output = json.loads(result.stdout)
        assert output["file"]["total_rows"] == 3


class TestBackwardCompatibility:
    """Test backward compatibility with old CLI syntax."""

    def test_classify_without_subcommand(self, sample_csv_file):
        """Test that old syntax (without subcommand) still works."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "email_classifier.cli",
                    str(sample_csv_file),
                    "-o",
                    tmpdir,
                    "--quiet",
                ],
                capture_output=True,
                text=True,
            )

            # Should succeed with backward compatible syntax
            assert result.returncode == 0

    def test_classify_with_subcommand(self, sample_csv_file):
        """Test explicit classify subcommand."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "email_classifier.cli",
                    "classify",
                    str(sample_csv_file),
                    "-o",
                    tmpdir,
                    "--quiet",
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0

    def test_help_shows_subcommands(self):
        """Test that help shows available subcommands."""
        result = subprocess.run(
            [sys.executable, "-m", "email_classifier.cli", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "classify" in result.stdout
        assert "info" in result.stdout

    def test_info_help(self):
        """Test info subcommand help."""
        result = subprocess.run(
            [sys.executable, "-m", "email_classifier.cli", "info", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "--json" in result.stdout
        assert "--quiet" in result.stdout
