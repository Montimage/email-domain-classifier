# Security Policy

## Supported Versions

| Version | Supported | Security Updates |
|---------|-----------|------------------|
| 1.0.x   | ✅ Yes    | ✅ Yes           |
| < 1.0   | ❌ No     | ❌ No            |

## Reporting a Vulnerability

We take the security of the Email Domain Classifier seriously. If you discover a security vulnerability, please report it to us responsibly.

### How to Report

**Preferred Method**: Email our security team directly at `security@montimage.com`

**Alternative Method**: Create a private vulnerability report on GitHub

### What to Include

Please provide as much information as possible about the vulnerability:

1. **Vulnerability Type** (e.g., buffer overflow, injection, cross-site scripting)
2. **Affected Versions** of the software
3. **Detailed Description** of the vulnerability
4. **Steps to Reproduce** the issue
5. **Proof of Concept** or exploit code (if available)
6. **Potential Impact** of the vulnerability
7. **Suggested Mitigation** (if you have a solution)

### Example Report Template

```
Subject: Security Vulnerability Report - [Brief Description]

Vulnerability Type: [Type of vulnerability]
Affected Versions: [List affected versions]
Severity: [Critical/High/Medium/Low]

Description:
[Detailed description of the vulnerability]

Steps to Reproduce:
1. [Step one]
2. [Step two]
3. [Step three]

Impact:
[Explanation of potential impact]

Suggested Fix:
[Your suggested fix, if any]

Additional Information:
[Any other relevant details]
```

## Response Timeline

- **Initial Response**: Within 48 hours of receiving your report
- **Detailed Analysis**: Within 7 business days
- **Fix Release**: As soon as practical, based on severity
- **Public Disclosure**: After fix is released, with appropriate credit

## Security Measures

### Built-in Protections

The Email Domain Classifier includes several security measures:

1. **Input Validation**: CSV input is validated before processing
2. **Memory Management**: Streaming processing prevents memory exhaustion
3. **Error Handling**: Graceful handling of malformed input data
4. **No Network Access**: Classifier operates entirely on local data
5. **No Arbitrary Code Execution**: Safe text processing only

### Recommended Practices

For users integrating the classifier:

1. **Input Validation**: Validate email data before classification
2. **Access Control**: Restrict access to classified output files
3. **Log Security**: Protect classification logs containing sensitive data
4. **Regular Updates**: Keep the package updated to the latest version
5. **Environment Isolation**: Run in isolated environments when possible

## Security Updates

### How We Handle Updates

1. **Vulnerability Assessment**: Each report is evaluated for severity and impact
2. **Priority Classification**: Critical > High > Medium > Low
3. **Fix Development**: Patches are developed following secure coding practices
4. **Testing**: Comprehensive testing including security regression tests
5. **Release**: Security updates are released as soon as possible
6. **Disclosure**: Public disclosure coordinated with reporters

### Update Channels

- **PyPI**: Security updates published to Python Package Index
- **GitHub Releases**: Security releases tagged and documented
- **Security Advisories**: GitHub Security Advisories for disclosed vulnerabilities

## Coordinated Disclosure

We follow responsible disclosure practices:

1. **Private Coordination**: Work with reporters privately during fix development
2. **Reasonable Timeline**: Allow sufficient time for fix development and testing
3. **Credit Recognition**: Acknowledge contributors who discover vulnerabilities
4. **Clear Communication**: Provide clear information about fixes and mitigations

## Security Best Practices

### For Developers

1. **Input Sanitization**: Always validate and sanitize input data
2. **Error Handling**: Implement proper error handling without information disclosure
3. **Dependency Management**: Keep dependencies updated and vet them for security
4. **Code Review**: Follow secure code review practices
5. **Testing**: Include security tests in your test suite

### For Users

1. **Least Privilege**: Run with minimal necessary permissions
2. **Input Validation**: Validate data before classification
3. **Secure Storage**: Store classified output securely
4. **Access Control**: Implement proper access controls for classified data
5. **Monitoring**: Monitor for unusual activity in classification processes

## Common Security Considerations

### Data Privacy

- The classifier processes email content locally
- No data is transmitted to external services
- Output files contain classified email content
- Log files may contain sensitive information from input data

### Resource Security

- Memory usage is controlled through streaming processing
- No network connections are made during classification
- File I/O is restricted to specified input/output directories
- CPU usage is proportional to input data size

### Third-Party Dependencies

- Limited external dependencies reduce attack surface
- Dependencies are regularly updated for security
- Each dependency is evaluated for security implications
- Automated scanning detects vulnerable dependencies

## Security Team

Our security team is responsible for:

- **Vulnerability Assessment**: Evaluating and triaging security reports
- **Fix Development**: Creating and testing security patches
- **Coordination**: Working with researchers and the community
- **Documentation**: Maintaining security documentation and advisories
- **Compliance**: Ensuring security best practices are followed

## Acknowledgments

We thank all security researchers who help us keep the Email Domain Classifier secure. Your contributions are invaluable to maintaining the security and trustworthiness of our software.

## Legal Notice

Please report security vulnerabilities responsibly. Do not:

- Exploit vulnerabilities without permission
- Disclose vulnerabilities publicly before coordinated disclosure
- Use vulnerabilities to harm others or their systems
- Violate applicable laws during security research

By following responsible disclosure practices, you help us maintain security for all users.

---

For questions about this security policy or to report a security issue, contact us at `security@montimage.com`.
