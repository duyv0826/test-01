# Contributing to test-01

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (if available).

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in [Issues](https://github.com/duyv0826/test-01/issues)
- If not, create a new issue with a clear description and reproduction steps

### Suggesting Enhancements

- Open a new issue with the tag \enhancement\
- Describe the feature and why it would be useful

### Pull Requests

1. Fork the repository
2. Create your feature branch (\git checkout -b feature/AmazingFeature\)
3. Commit your changes (\git commit -m 'Add some AmazingFeature'\)
4. Push to the branch (\git push origin feature/AmazingFeature\)
5. Open a Pull Request

## Development Setup

\\\ash
# Clone the repository
git clone https://github.com/duyv0826/test-01.git
cd test-01

# Create virtual environment (for Python projects)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # if applicable
\\\

## Coding Standards

- Write clear, readable code
- Follow PEP 8 for Python code
- Add comments where necessary
- Write tests for new features
- Update documentation as needed

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (e.g., \"Add\", \"Fix\", \"Update\")
- Reference issue numbers when applicable

Example:
\\\
Add user authentication feature

- Implements login/logout functionality
- Adds password hashing
- Closes #42
\\\

## Testing

- Run existing tests before submitting PR
- Add new tests for new functionality
- Ensure all tests pass

\\\ash
# Run tests
python -m pytest tests/
\\\

## License

By contributing, you agree that your contributions will be licensed under the same [Apache-2.0 License](LICENSE) that covers this project.

## Questions?

Feel free to open an issue with your question or contact the maintainers.

---

Thank you for contributing!