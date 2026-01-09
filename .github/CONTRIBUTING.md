# Contributing to Connector (ServiceNow MCP Server)

Thank you for your interest in contributing to Connector! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/Kromula/Connector/issues)
2. If not, create a new issue using the Bug Report template
3. Provide as much detail as possible, including:
   - Clear reproduction steps
   - Expected vs actual behavior
   - Environment details
   - Error messages or logs

### Suggesting Enhancements
1. Check if the enhancement has already been suggested
2. Create a new issue using the Feature Request template
3. Explain the use case and benefits
4. Provide examples of how it would work

### Submitting Code Changes

#### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/Kromula/Connector.git
cd Connector

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Set up your ServiceNow instance
cp config/instances.yaml.example config/instances.yaml
# Edit config/instances.yaml with your test instance
```

#### Making Changes
1. Fork the repository
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. Make your changes following the code style guidelines
4. Test your changes thoroughly
5. Commit your changes with clear, descriptive messages
6. Push to your fork
7. Submit a pull request

#### Code Style Guidelines
- Follow PEP 8 style guide for Python code
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

#### Testing
- Test with multiple ServiceNow instances if possible
- Test both MFA and non-MFA authentication flows
- Verify session caching works correctly
- Test error handling and edge cases

#### Commit Message Format
```
<type>: <short summary>

<detailed description>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat: Add support for custom timeout in MFA authentication

Allow users to configure MFA timeout duration in instances.yaml
config file. Defaults to 300 seconds (5 minutes) if not specified.

Closes #42
```

### Pull Request Guidelines
1. Reference related issues in your PR description
2. Describe what changes you made and why
3. Include any breaking changes or migration notes
4. Ensure all tests pass
5. Update documentation if needed
6. Keep PRs focused - one feature/fix per PR

## Code Review Process
1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged in release notes

## Development Priorities

### High Priority
- Bug fixes affecting core functionality
- Security vulnerabilities
- Authentication and session management issues
- MCP tool reliability

### Medium Priority
- New MCP tools for ServiceNow operations
- CLI enhancements
- Performance improvements
- Documentation improvements

### Low Priority
- Code refactoring (without functional changes)
- Style improvements
- Optional features

## Questions or Help
If you need help or have questions:
1. Check the [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)
2. Search existing [Issues](https://github.com/Kromula/Connector/issues)
3. Create a new issue using the Question template

## License
By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition
All contributors will be acknowledged in:
- CHANGELOG.md
- Release notes
- GitHub contributors page

Thank you for contributing to Connector!
