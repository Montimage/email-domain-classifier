"""
Email validation and invalid email handling.

Provides validation for email records before classification,
ensuring data quality by checking email format and required fields.
"""

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Any, Dict, List, Literal, Optional, Tuple


@dataclass
class ValidationResult:
    """Result of email validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)


@dataclass
class ValidationStats:
    """Statistics for validation failures."""

    total_invalid: int = 0
    invalid_sender_format: int = 0
    invalid_receiver_format: int = 0
    invalid_empty_sender: int = 0
    invalid_empty_receiver: int = 0
    invalid_empty_subject: int = 0
    invalid_empty_body: int = 0

    def to_dict(self) -> dict:
        """Convert stats to dictionary."""
        return {
            "total_invalid": self.total_invalid,
            "invalid_sender_format": self.invalid_sender_format,
            "invalid_receiver_format": self.invalid_receiver_format,
            "invalid_empty_sender": self.invalid_empty_sender,
            "invalid_empty_receiver": self.invalid_empty_receiver,
            "invalid_empty_subject": self.invalid_empty_subject,
            "invalid_empty_body": self.invalid_empty_body,
        }


@dataclass
class SkippedStats:
    """Statistics for skipped emails due to filtering."""

    total_skipped: int = 0
    skipped_body_too_long: int = 0

    def to_dict(self) -> dict:
        """Convert stats to dictionary."""
        return {
            "total_skipped": self.total_skipped,
            "skipped_body_too_long": self.skipped_body_too_long,
        }


class EmailValidator:
    """
    Validates email records before processing.

    Checks:
    - Sender email format
    - Receiver email format
    - Non-empty subject
    - Non-empty body
    """

    # Simplified RFC 5322 email pattern for practical use
    # Matches: user@domain.com
    EMAIL_PATTERN = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", re.IGNORECASE
    )

    # Pattern for "Display Name <email@domain.com>" format
    # Matches: John Doe <john@example.com> or "John Doe" <john@example.com>
    EMAIL_WITH_NAME_PATTERN = re.compile(
        r"^[^<]*<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>$", re.IGNORECASE
    )

    def validate_email_format(self, email: str) -> bool:
        """
        Validate email address format.

        Accepts both plain email addresses and "Name <email>" format:
        - user@example.com
        - John Doe <john@example.com>
        - "John Doe" <john@example.com>

        Args:
            email: Email address string to validate

        Returns:
            True if email format is valid, False otherwise
        """
        if not email or not email.strip():
            return False

        email = email.strip()

        # First try plain email format
        if self.EMAIL_PATTERN.match(email):
            return True

        # Then try "Name <email>" format
        if self.EMAIL_WITH_NAME_PATTERN.match(email):
            return True

        return False

    def validate(self, email_dict: dict) -> ValidationResult:
        """
        Validate an email record.

        Args:
            email_dict: Dictionary containing email fields

        Returns:
            ValidationResult with is_valid flag and list of errors
        """
        errors = []

        # Validate sender
        sender = str(email_dict.get("sender", "")).strip()
        if not sender:
            errors.append("empty_sender")
        elif not self.validate_email_format(sender):
            errors.append("invalid_sender_format")

        # Validate receiver
        receiver = str(email_dict.get("receiver", "")).strip()
        if not receiver:
            errors.append("empty_receiver")
        elif not self.validate_email_format(receiver):
            errors.append("invalid_receiver_format")

        # Validate subject (non-empty)
        subject = str(email_dict.get("subject", "")).strip()
        if not subject:
            errors.append("empty_subject")

        # Validate body (non-empty)
        body = str(email_dict.get("body", "")).strip()
        if not body:
            errors.append("empty_body")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class InvalidEmailWriter:
    """
    Writes invalid emails to a separate CSV file for review.

    Creates invalid_emails.csv with original columns plus validation_errors.
    """

    def __init__(self, output_dir: Path, fieldnames: list[str]):
        """
        Initialize the invalid email writer.

        Args:
            output_dir: Directory to write invalid_emails.csv
            fieldnames: List of column names from input CSV
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.output_dir / "invalid_emails.csv"
        self.fieldnames = list(fieldnames) + ["validation_errors"]
        self.file: IO[str] | None = None
        self.writer: csv.DictWriter[str] | None = None
        self.stats = ValidationStats()

    def _ensure_writer(self) -> None:
        """Create CSV writer if not already created."""
        if self.writer is None:
            self.file = open(self.filepath, "w", newline="", encoding="utf-8")
            self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
            self.writer.writeheader()

    def write(self, email_dict: dict[str, Any], errors: list[str]) -> None:
        """
        Write an invalid email record to the CSV file.

        Args:
            email_dict: Original email data
            errors: List of validation error codes
        """
        self._ensure_writer()

        # Prepare row with original data plus errors
        row: dict[str, Any] = {
            k: email_dict.get(k, "")
            for k in self.fieldnames
            if k != "validation_errors"
        }
        row["validation_errors"] = "|".join(errors)

        if self.writer is not None:
            self.writer.writerow(row)
        if self.file is not None:
            self.file.flush()

        # Update statistics
        self.stats.total_invalid += 1
        for error in errors:
            if error == "invalid_sender_format":
                self.stats.invalid_sender_format += 1
            elif error == "invalid_receiver_format":
                self.stats.invalid_receiver_format += 1
            elif error == "empty_sender":
                self.stats.invalid_empty_sender += 1
            elif error == "empty_receiver":
                self.stats.invalid_empty_receiver += 1
            elif error == "empty_subject":
                self.stats.invalid_empty_subject += 1
            elif error == "empty_body":
                self.stats.invalid_empty_body += 1

    def close(self) -> None:
        """Close the CSV file."""
        if self.file is not None:
            self.file.close()
            self.file = None
            self.writer = None

    def get_stats(self) -> ValidationStats:
        """Get validation statistics."""
        return self.stats

    def __enter__(self) -> "InvalidEmailWriter":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]:
        self.close()
        return False


class SkippedEmailWriter:
    """
    Writes skipped emails to a separate CSV file for review.

    Creates skipped_emails.csv with original columns plus skip_reason.
    """

    def __init__(self, output_dir: Path, fieldnames: list[str]):
        """
        Initialize the skipped email writer.

        Args:
            output_dir: Directory to write skipped_emails.csv
            fieldnames: List of column names from input CSV
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.output_dir / "skipped_emails.csv"
        self.fieldnames = list(fieldnames) + ["skip_reason"]
        self.file: IO[str] | None = None
        self.writer: csv.DictWriter[str] | None = None
        self.stats = SkippedStats()

    def _ensure_writer(self) -> None:
        """Create CSV writer if not already created."""
        if self.writer is None:
            self.file = open(self.filepath, "w", newline="", encoding="utf-8")
            self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
            self.writer.writeheader()

    def write(self, email_dict: dict[str, Any], reason: str) -> None:
        """
        Write a skipped email record to the CSV file.

        Args:
            email_dict: Original email data
            reason: Reason for skipping (e.g., "body_too_long")
        """
        self._ensure_writer()

        # Prepare row with original data plus reason
        row: dict[str, Any] = {
            k: email_dict.get(k, "") for k in self.fieldnames if k != "skip_reason"
        }
        row["skip_reason"] = reason

        if self.writer is not None:
            self.writer.writerow(row)
        if self.file is not None:
            self.file.flush()

        # Update statistics
        self.stats.total_skipped += 1
        if reason == "body_too_long":
            self.stats.skipped_body_too_long += 1

    def close(self) -> None:
        """Close the CSV file."""
        if self.file is not None:
            self.file.close()
            self.file = None
            self.writer = None

    def get_stats(self) -> SkippedStats:
        """Get skipped email statistics."""
        return self.stats

    def __enter__(self) -> "SkippedEmailWriter":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]:
        self.close()
        return False
