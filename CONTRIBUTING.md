# Contributing to Recon Automation Tool

First off, thank you for considering contributing to Recon Automation Tool! It's people like you that make this tool better for the cybersecurity community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Security Vulnerabilities](#security-vulnerabilities)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## 💡 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Description:**
A clear description of the bug

**To Reproduce:**
Steps to reproduce the behavior:
1. Run command '...'
2. With target '...'
3. See error

**Expected Behavior:**
What you expected to happen

**Screenshots/Output:**
If applicable, add screenshots or terminal output

**Environment:**
- OS: [e.g., Kali Linux 2024.1]
- Python Version: [e.g., 3.11.2]
- Tool Version: [e.g., 1.0.0]

**Additional Context:**
Any other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- A detailed description of the proposed feature
- Explain why this enhancement would be useful
- List any potential drawbacks or concerns

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Documentation improvements
- `enhancement` - New features or improvements

## 🔧 Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Linux-based OS (Ubuntu, Kali, Parrot, etc.)

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/recon-tool.git
cd recon-tool

# 3. Add upstream remote
git remote add upstream https://github.com/original-owner/recon-tool.git

# 4. Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Install development dependencies
pip3 install pytest black flake8 pylint

# 7. Create a feature branch
git checkout -b feature/your-feature-name
```

### Running Tests

```bash
# Run the tool with test target
python3 recon.py -u example.com

# Test specific modules
python3 recon.py -u example.com --no-subdomains --no-whois

# Verify all dependencies
python3 -c "import dns.resolver, requests, whois; print('All dependencies OK')"
```

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings unless double quotes avoid escaping
- **Imports**: Organized as: standard library, third-party, local

### Code Formatting

```bash
# Format code with black
black recon.py --line-length 100

# Check with flake8
flake8 recon.py --max-line-length=100

# Lint with pylint
pylint recon.py
```

### Documentation Standards

- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Comments**: Write clear, concise comments explaining "why", not "what"
- **Type Hints**: Use type hints where appropriate (Python 3.7+)

Example:

```python
def scan_port(self, port: int) -> dict:
    """
    Scan a single port on the target.
    
    Args:
        port (int): The port number to scan
        
    Returns:
        dict: Dictionary containing port info if open, None otherwise
        
    Raises:
        socket.error: If connection fails unexpectedly
    """
    # Implementation here
```

### Security Best Practices

- Never hardcode credentials or API keys
- Validate all user inputs
- Use secure defaults
- Handle sensitive data appropriately
- Add rate limiting where applicable
- Implement proper error handling

## 📋 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(scanner): add SSL/TLS certificate analysis

Add functionality to extract and display SSL certificate
information including issuer, validity dates, and cipher suites.

Closes #123

---

fix(dns): handle NXDOMAIN exceptions properly

Previously, NXDOMAIN errors would crash the application.
Now they are caught and reported gracefully.

---

docs(readme): update installation instructions

Add troubleshooting section and improve clarity of setup steps.
```

### Commit Best Practices

- Make atomic commits (one logical change per commit)
- Write clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused and small

## 🚀 Pull Request Process

### Before Submitting

1. **Update Documentation**: Update README.md if you changed functionality
2. **Test Thoroughly**: Test your changes on multiple systems if possible
3. **Follow Style Guide**: Ensure code follows project standards
4. **Update CHANGELOG**: Add entry to CHANGELOG.md
5. **Rebase on Latest**: Ensure your branch is up to date

```bash
git fetch upstream
git rebase upstream/main
```

### PR Submission Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added to complex sections
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for new features
- [ ] All tests passing
- [ ] CHANGELOG.md updated

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots of new features

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added
- [ ] Documentation updated
- [ ] Tests passing
```

### Review Process

1. At least one maintainer must approve the PR
2. All CI checks must pass
3. No merge conflicts
4. Discussion and feedback will be provided
5. Changes may be requested before merge

## 🔐 Security Vulnerabilities

**DO NOT** create public issues for security vulnerabilities.

Instead, please email security details to: security@example.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## 📚 Additional Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)

## 🎯 Priority Areas

We're particularly interested in contributions in these areas:

1. **Performance Optimization**: Speed improvements
2. **New Reconnaissance Modules**: Additional scanning capabilities
3. **Output Formats**: New report formats or visualizations
4. **Error Handling**: Improved error messages and handling
5. **Documentation**: Tutorials, examples, translations
6. **Testing**: Unit tests, integration tests

## ❓ Questions?

- Check existing [GitHub Issues](https://github.com/yourusername/recon-tool/issues)
- Start a [Discussion](https://github.com/yourusername/recon-tool/discussions)
- Join our community chat (if applicable)

## 🙏 Recognition

Contributors will be recognized in:
- README.md Contributors section
- CHANGELOG.md for their contributions
- GitHub contributors graph

Thank you for contributing to making reconnaissance more efficient and accessible!

---

**Happy Coding! 🚀**
