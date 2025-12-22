#!/usr/bin/env python3
"""
Email Domain Classifier - Setup Configuration

Install with:
    pip install -e .

Or for development:
    pip install -e ".[dev]"
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = (
    readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
)

setup(
    name="email-classifier",
    version="1.0.0",
    author="Montimage Security Research",
    author_email="research@montimage.com",
    description="Classify emails by domain using dual-method validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luongnv89/email-classifier",
    packages=["email_classifier"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Communications :: Email",
    ],
    python_requires=">=3.10",
    install_requires=[
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-classifier=email_classifier.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
