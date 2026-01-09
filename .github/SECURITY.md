# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Connector, please report it by emailing the maintainers or creating a private security advisory on GitHub.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

When reporting a security vulnerability, please include:

1. **Type of vulnerability** (e.g., authentication bypass, injection, exposure of sensitive data)
2. **Full description** of the vulnerability and its impact
3. **Steps to reproduce** the issue
4. **Affected version(s)**
5. **Potential fix** (if you have suggestions)

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 30 days
  - Medium/Low: Next scheduled release

## Security Best Practices

### For Users

1. **Credentials Management**
   - Never commit `config/instances.yaml` with real credentials
   - Use environment variables for passwords when possible
   - Rotate passwords regularly
   - Use strong, unique passwords

2. **Session Security**
   - Review session cache duration based on your security requirements
   - Clear cached sessions when changing passwords
   - Set appropriate file permissions on cache directory (Unix: 700)

3. **Network Security**
   - Always use HTTPS URLs for ServiceNow instances
   - Verify SSL certificates
   - Use firewalls and VPNs when accessing sensitive instances

4. **Instance Configuration**
   - Keep `config/instances.yaml` file permissions restricted
   - Regularly review configured instances
   - Remove unused instance configurations

5. **Updates**
   - Keep the Connector up to date with latest security patches
   - Monitor the repository for security advisories
   - Review CHANGELOG for security-related updates

### For Developers

1. **Code Security**
   - Never log sensitive information (passwords, session tokens)
   - Validate all user inputs
   - Use parameterized queries
   - Follow secure coding practices

2. **Dependencies**
   - Regularly update dependencies
   - Monitor for security advisories in dependencies
   - Use `pip audit` or similar tools

3. **Testing**
   - Include security tests in test suites
   - Test authentication flows thoroughly
   - Verify proper error handling

4. **Code Review**
   - All code changes should be reviewed
   - Pay special attention to authentication and session management
   - Look for potential injection points

## Known Security Considerations

### Session Caching
- Sessions are cached locally in JSON format
- Cache files should have restricted permissions
- Sessions expire after configured duration (default: 8 hours)
- Consider your security requirements when setting cache duration

### MFA
- MFA approval timeout is 5 minutes
- Multiple failed authentication attempts are not rate-limited (future enhancement)
- MFA is instance-dependent (controlled by ServiceNow)

### Passwords in Configuration
- Passwords in YAML files are plain text
- Environment variables are recommended alternative
- Consider using a secrets manager for production use

## Future Security Enhancements

Planned improvements:
- [ ] OAuth 2.0 support (Issue #1)
- [ ] Encrypted session cache
- [ ] Rate limiting for authentication attempts
- [ ] Audit logging
- [ ] Integration with system keychains/credential managers
- [ ] Two-factor authentication for CLI access

## Security Contacts

For security-related questions or concerns:
- Create a private security advisory on GitHub
- Contact the maintainers directly

## Disclosure Policy

Once a security vulnerability is fixed:
1. We will release a patch
2. Publish a security advisory
3. Credit the reporter (if desired)
4. Update CHANGELOG with security fix details

Thank you for helping keep Connector secure!
