"""Tests for domain definitions and profiles."""

import pytest
from email_classifier.domains import DOMAINS, get_domain_names, get_domain_profile


class TestDomains:
    """Test cases for domain definitions."""

    def test_domains_available(self):
        """Test that domains are properly defined."""
        assert len(DOMAINS) > 0
        assert "finance" in DOMAINS
        assert "technology" in DOMAINS

    def test_get_domain_names(self):
        """Test get_domain_names function."""
        names = get_domain_names()
        assert isinstance(names, list)
        assert len(names) > 0
        assert "finance" in names

    def test_get_domain_profile(self):
        """Test get_domain_profile function."""
        profile = get_domain_profile("finance")
        assert profile is not None
        assert hasattr(profile, "name")
        assert profile.name == "finance"

    def test_get_domain_profile_invalid(self):
        """Test get_domain_profile with invalid domain."""
        profile = get_domain_profile("invalid_domain")
        assert profile is None
