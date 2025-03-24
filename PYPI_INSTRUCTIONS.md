# Publishing to PyPI

This document explains how to publish the doi-finder package to PyPI.

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Install required tools:
   ```bash
   pip install build twine
   ```

## Option 1: Using the Provided Script

We've included a script to make publishing easier:

```bash
python publish_to_pypi.py
```

This script will:
1. Clean build directories
2. Build the package
3. Validate the package
4. Offer to upload to Test PyPI first (recommended)
5. Offer to upload to PyPI

## Option 2: Manual Publishing

If you prefer to do it manually, follow these steps:

### 1. Clean Up Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### 2. Build the Package

```bash
python -m build
```

This will create:
- Source distribution (`dist/*.tar.gz`)
- Wheel distribution (`dist/*.whl`)

### 3. Check the Package

```bash
twine check dist/*
```

### 4. Upload to Test PyPI (Optional but Recommended)

```bash
twine upload --repository testpypi dist/*
```

Then test the installation:
```bash
pip install --index-url https://test.pypi.org/simple/ doi-finder
```

### 5. Upload to PyPI

```bash
twine upload dist/*
```

## Authentication

When uploading to PyPI, you need to authenticate. You have several options:

### 1. Username and Password

Twine will prompt for your PyPI username and password.

### 2. API Token (Recommended)

1. Generate an API token at https://pypi.org/manage/account/token/
2. Create a `~/.pypirc` file:
   ```
   [pypi]
   username = __token__
   password = pypi-your-token-goes-here

   [testpypi]
   username = __token__
   password = pypi-your-test-token-goes-here
   ```

## Releasing New Versions

When releasing a new version:

1. Update the version number in:
   - `pyproject.toml`
   - `setup.py`

2. Create a git tag for the release:
   ```bash
   git tag -a v0.1.0 -m "Version 0.1.0"
   git push origin v0.1.0
   ```

3. Follow the publishing steps above 