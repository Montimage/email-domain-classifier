## Description
<!-- Brief description of changes made in this pull request -->

## Type of Change
Please select relevant options:

- [ ] **Bug fix** (non-breaking change that fixes an issue)
- [ ] **New feature** (non-breaking change that adds functionality)
- [ ] **Breaking change** (fix or feature that would cause existing functionality to not work as expected)
- [ ] **Documentation update** (documentation only changes)
- [ ] **Refactoring** (code changes that neither fix a bug nor add a feature)
- [ ] **Performance improvement** (code changes that improve performance)
- [ ] **Code quality** (code changes that improve maintainability, readability, etc.)
- [ ] **Tests** (adding or updating tests)
- [ ] **Build/CI** (changes to build process or continuous integration)

## Related Issue(s)
<!-- If this PR addresses any open issues, reference them here -->
Closes #
Fixes #
Related to #

## Changes Made
<!-- List specific changes made in this pull request -->

### Code Changes
- [ ] Modified existing code
- [ ] Added new code
- [ ] Removed code

### Files Modified
<!-- List files that were modified -->
- 

### Files Added
<!-- List new files that were added -->
- 

### Files Removed
<!-- List files that were removed -->
- 

## Testing
<!-- Describe how you tested your changes -->

### Manual Testing
- [ ] Tested CLI functionality with sample data
- [ ] Tested edge cases and error conditions
- [ ] Verified backward compatibility (if applicable)
- [ ] Tested on multiple operating systems (if applicable)

### Automated Testing
- [ ] Added new unit tests
- [ ] Added new integration tests
- [ ] Updated existing tests
- [ ] All tests pass locally: `pytest --cov=email_classifier`

### Test Commands Used
<!-- List commands you used for testing -->
```bash
# Example test commands
pytest tests/
email-cli sample_emails.csv -o test_output/
black --check .
isort --check-only .
mypy email_classifier/
```

## Code Quality
<!-- Confirm code quality standards -->

### Code Style
- [ ] Code follows project coding standards
- [ ] Code has been formatted with `black .`
- [ ] Imports have been sorted with `isort .`
- [ ] Type checking passes with `mypy email_classifier/`

### Documentation
- [ ] Added or updated docstrings for new/modified functions
- [ ] Updated README.md if needed
- [ ] Updated CHANGELOG.md if this is a user-facing change
- [ ] Added or updated inline comments where necessary

### Breaking Changes
<!-- If there are breaking changes, describe them in detail -->
- [ ] This PR includes breaking changes
- [ ] Migration guide has been provided
- [ ] Documentation has been updated to reflect changes

## Performance Impact
<!-- Describe any performance implications -->

- [ ] This change improves performance
- [ ] This change has no performance impact
- [ ] This change may impact performance (describe how)

## Security Considerations
<!-- Address any security implications -->

- [ ] This change has security implications
- [ ] Security review has been conducted
- [ ] SECURITY.md has been updated if needed

## Checklist
<!-- Review these items before submitting -->

### Pre-submission Checks
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules

### Post-submission
- [ ] I have checked that all CI checks pass
- [ ] I am ready to respond to reviewer feedback
- [ ] I will update documentation based on review feedback

## Additional Context
<!-- Add any other context, screenshots, or examples about the pull request here -->

### Screenshots
<!-- If applicable, add screenshots to help explain your changes -->
<!-- Add screenshots here -->

### Example Usage
<!-- If this is a new feature, provide example usage -->
```bash
# Example CLI usage
email-cli input.csv -o output/ --new-feature

# Example Python usage
from email_classifier import EmailClassifier
# Your example code here
```

### Performance Benchmarks
<!-- If relevant, include performance measurements -->
<!-- 
Before: X seconds
After: Y seconds
Improvement: Z%
-->

## Reviewer Guidance
<!-- What should reviewers focus on when reviewing this PR? -->

1. 
2. 
3. 

## Release Notes
<!-- If this is a user-facing change, add release notes -->

### Added
- 

### Changed
- 

### Fixed
- 

### Deprecated
- 

### Removed
- 

### Security
- 

---

Thank you for contributing to Email Domain Classifier! 🎉