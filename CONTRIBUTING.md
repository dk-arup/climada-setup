# Contributing to CLIMADA Setup

Thank you for your interest in contributing to the CLIMADA Setup project! This guide will help you get started.

## Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/climada-setup.git
   cd climada-setup
   ```

2. **Set Up Environment**
   ```bash
   mamba env create -f environment.yml
   mamba activate climada_env
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Adding Workflows

When adding new workflow scripts:

1. **Place in `workflows/` directory** with a numbered prefix (e.g., `06_new_workflow.py`)
2. **Include comprehensive docstrings** at the top of the file
3. **Add error handling** for missing dependencies
4. **Provide example output** or visualizations when possible
5. **Update README.md** to reference the new workflow

### Example Workflow Structure

```python
#!/usr/bin/env python3
"""
Brief Description of Workflow

Detailed explanation of what this workflow demonstrates:
1. First step
2. Second step
3. Third step

Author: Your Name
Date: YYYY-MM-DD
"""

import sys

try:
    from climada.entity import Exposures
    # ... other imports
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure CLIMADA is properly installed.")
    sys.exit(1)

def main():
    """Main workflow execution."""
    print("=" * 60)
    print("Workflow Title")
    print("=" * 60)
    
    # Your code here
    
    print("\nWorkflow completed!")

if __name__ == "__main__":
    main()
```

### Documentation

- Update README.md for major changes
- Add inline comments for complex logic
- Create or update Jupyter notebooks for interactive examples
- Include links to relevant CLIMADA documentation

### Data Files

- **Do not commit large data files** to the repository
- Use `.gitignore` to exclude data files
- Document where to obtain required datasets
- Provide small example datasets when necessary

## Testing

Before submitting a pull request:

1. **Test your code**
   ```bash
   python your_script.py
   ```

2. **Check for syntax errors**
   ```bash
   python -m py_compile your_script.py
   ```

3. **Verify imports work** (if CLIMADA is installed)
   ```bash
   python -c "from climada.entity import Exposures"
   ```

4. **Test without CLIMADA** to ensure graceful error handling
   ```bash
   # In a clean environment without CLIMADA
   python your_script.py
   ```

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes clearly
   - Link any related issues

### Pull Request Guidelines

- **Clear title**: Briefly describe what the PR does
- **Detailed description**: Explain the changes and why they're needed
- **Reference issues**: Link to related issues using `#issue_number`
- **Test results**: Mention any testing you've done
- **Screenshots**: Include for UI or visualization changes

## Types of Contributions

### Bug Fixes

- Report bugs via GitHub Issues
- Include steps to reproduce
- Provide environment details (OS, Python version, CLIMADA version)

### New Workflows

- Propose new workflow ideas via GitHub Issues first
- Ensure they demonstrate practical CLIMADA use cases
- Focus on educational value

### Documentation Improvements

- Fix typos and clarify instructions
- Add examples and use cases
- Improve installation guides
- Translate documentation (future)

### Enhancement Ideas

- Improve existing workflows
- Add new utility functions
- Optimize performance
- Better error messages

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Follow the CLIMADA community guidelines

## Questions?

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **CLIMADA Documentation**: https://climada-python.readthedocs.io/
- **CLIMADA Community**: https://github.com/CLIMADA-project/climada_python/discussions

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project.

## Acknowledgments

- CLIMADA is developed by ETH Zurich's Weather and Climate Risks Group
- This setup repository builds upon CLIMADA's excellent documentation
- Thank you to all contributors!

---

**Happy Contributing! 🌍**
