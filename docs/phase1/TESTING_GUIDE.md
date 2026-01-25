# 🧪 Testing Guide - Cricket Analytics

## Overview

This document provides comprehensive information about testing in the cricket analytics project, including unit tests, integration tests, and CI/CD automation.

---

## 📋 Table of Contents

1. [Test Structure](#test-structure)
2. [Running Tests](#running-tests)
3. [Test Coverage](#test-coverage)
4. [Writing Tests](#writing-tests)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Troubleshooting](#troubleshooting)

---

## 🏗️ Test Structure

### Test Directory Layout

```
tests/
├── __init__.py                      # Test package initialization
├── conftest.py                      # Pytest fixtures and configuration
├── test_cricsheet_downloader.py    # Downloader tests
├── test_cricpy_loader.py           # Data loader tests
├── test_data_processing.py         # Integration tests
└── test_data/
    └── sample_match.yaml           # Sample test data
```

### Test Categories

1. **Unit Tests** - Test individual functions and modules
   - `test_cricsheet_downloader.py` - Downloader functionality
   - `test_cricpy_loader.py` - YAML loading and parsing

2. **Integration Tests** - Test complete workflows
   - `test_data_processing.py` - End-to-end data processing

3. **Data Quality Tests** - Validate processed datasets
   - Data structure validation
   - Value range checks
   - Consistency checks

---

## 🚀 Running Tests

### Prerequisites

Install testing dependencies:

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_cricsheet_downloader.py -v
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest tests/ -v -m unit

# Run only integration tests
pytest tests/ -v -m integration

# Skip slow tests
pytest tests/ -v -m "not slow"

# Skip network-dependent tests
pytest tests/ -v -m "not network"
```

### Run Specific Tests

```bash
# Run a specific test class
pytest tests/test_cricsheet_downloader.py::TestCricsheetDownloader -v

# Run a specific test method
pytest tests/test_cricsheet_downloader.py::TestCricsheetDownloader::test_list_available_tournaments -v
```

---

## 📊 Test Coverage

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=scripts --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Generate Terminal Coverage Report

```bash
pytest tests/ --cov=scripts --cov-report=term-missing
```

### Coverage Goals

- **Target**: 80%+ coverage for core modules
- **Critical paths**: 95%+ coverage for data processing
- **Utilities**: 70%+ coverage acceptable

---

## ✍️ Writing Tests

### Test Naming Conventions

```python
# Test file names
test_<module_name>.py

# Test class names
class Test<ClassName>:
    pass

# Test method names
def test_<what_is_being_tested>_<expected_behavior>():
    pass
```

### Example Unit Test

```python
import unittest
from scripts.cricsheet_downloader import CricsheetDownloader

class TestCricsheetDownloader(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.downloader = CricsheetDownloader()

    def test_list_tournaments_returns_dict(self):
        """Test that list_available_tournaments returns a dictionary"""
        tournaments = self.downloader.list_available_tournaments()

        self.assertIsInstance(tournaments, dict)
        self.assertGreater(len(tournaments), 0)

    def test_invalid_tournament_raises_error(self):
        """Test that invalid tournament name raises ValueError"""
        with self.assertRaises(ValueError):
            self.downloader.get_download_url('invalid_tournament')
```

### Using Pytest Fixtures

```python
import pytest

def test_with_sample_data(sample_match_data):
    """Test using the sample_match_data fixture"""
    assert 'info' in sample_match_data
    assert sample_match_data['info']['match_type'] == 'T20'

def test_with_temp_directory(temp_directory):
    """Test using temporary directory fixture"""
    test_file = temp_directory / 'test.txt'
    test_file.write_text('test content')
    assert test_file.exists()
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

@patch('cricsheet_downloader.requests.get')
def test_download_with_mock(mock_get):
    """Test download with mocked HTTP request"""
    # Configure mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Test code here
    # ...
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

The project uses three main CI/CD workflows:

#### 1. Tests Workflow (`.github/workflows/tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Actions:**
- Runs tests on multiple OS (Ubuntu, Windows, macOS)
- Tests Python versions 3.8, 3.9, 3.10, 3.11
- Generates coverage reports
- Uploads coverage to Codecov
- Runs code quality checks (flake8, black, isort)

**Usage:**
```bash
# Automatically runs on push/PR
# View results in GitHub Actions tab
```

#### 2. Data Validation Workflow (`.github/workflows/data-validation.yml`)

**Triggers:**
- Push to `main` branch
- Changes to `scripts/**` or `data/processed/**`
- Weekly schedule (Mondays at 9 AM UTC)
- Manual trigger

**Actions:**
- Validates processed data structure
- Runs data quality checks
- Tests data processing pipeline

**Manual Trigger:**
```bash
# Go to GitHub Actions → Data Validation → Run workflow
```

#### 3. Documentation Workflow (`.github/workflows/docs.yml`)

**Triggers:**
- Push to `main` branch with markdown changes
- Pull requests with documentation changes

**Actions:**
- Validates markdown files
- Checks for broken links
- Verifies README completeness
- Finds TODO/FIXME comments

#### 4. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Git tags matching `v*.*.*` pattern
- Manual workflow dispatch

**Actions:**
- Runs full test suite
- Creates GitHub release
- Generates release notes
- Publishes artifacts

**Create a Release:**
```bash
# Tag a version
git tag v1.0.0
git push origin v1.0.0

# Or manually trigger from GitHub Actions
```

---

## 🎯 Test Best Practices

### 1. Keep Tests Independent

```python
# Good - each test is independent
def test_function_a():
    result = function_a()
    assert result == expected

def test_function_b():
    result = function_b()
    assert result == expected

# Bad - tests depend on each other
shared_state = None

def test_setup():
    global shared_state
    shared_state = setup()

def test_using_shared_state():  # Depends on test_setup
    assert shared_state is not None
```

### 2. Use Descriptive Names

```python
# Good
def test_download_tournament_with_invalid_name_raises_value_error():
    pass

# Bad
def test_download():
    pass
```

### 3. Follow AAA Pattern

```python
def test_function():
    # Arrange - Set up test data
    downloader = CricsheetDownloader()
    tournament = 'ipl'

    # Act - Execute the function
    result = downloader.get_tournament_info(tournament)

    # Assert - Verify the outcome
    assert result['name'] == 'ipl'
    assert 'url' in result
```

### 4. Test Edge Cases

```python
def test_parse_match_with_empty_data():
    """Test handling of empty match data"""
    empty_match = {'info': {}, 'innings': []}
    result = parse_match(empty_match)
    assert len(result) == 0

def test_parse_match_with_missing_fields():
    """Test handling of missing optional fields"""
    minimal_match = {'info': {'venue': 'Test'}}
    result = parse_match_info(minimal_match)
    assert 'venue' in result
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: Tests fail with import errors

**Solution:**
```bash
# Ensure scripts directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts"

# Or install package in development mode
pip install -e .
```

#### Issue: Coverage report shows 0%

**Solution:**
```bash
# Install coverage
pip install pytest-cov

# Run with explicit source
pytest tests/ --cov=scripts --cov-report=term
```

#### Issue: Slow test execution

**Solution:**
```bash
# Skip slow tests
pytest tests/ -m "not slow"

# Run in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest tests/ -n auto
```

#### Issue: Network tests fail offline

**Solution:**
```bash
# Skip network-dependent tests
pytest tests/ -m "not network"
```

---

## 📈 Continuous Integration Status

### GitHub Actions Badges

Add these to your README.md:

```markdown
![Tests](https://github.com/yourusername/cricket-analytics/workflows/Tests/badge.svg)
![Data Validation](https://github.com/yourusername/cricket-analytics/workflows/Data%20Validation/badge.svg)
![Documentation](https://github.com/yourusername/cricket-analytics/workflows/Documentation/badge.svg)
```

### Codecov Integration

Coverage reports are automatically uploaded to Codecov on successful CI runs.

View coverage: `https://codecov.io/gh/yourusername/cricket-analytics`

---

## 🔧 Advanced Testing

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("tournament,expected_format", [
    ('ipl', 'YAML'),
    ('bbl', 'YAML'),
    ('t20_internationals_male', 'YAML'),
])
def test_tournament_formats(tournament, expected_format):
    downloader = CricsheetDownloader()
    info = downloader.get_tournament_info(tournament)
    assert info['format'] == expected_format
```

### Performance Testing

```python
import time

def test_download_performance():
    """Test that tournament list is retrieved quickly"""
    downloader = CricsheetDownloader()

    start_time = time.time()
    tournaments = downloader.list_available_tournaments()
    elapsed = time.time() - start_time

    assert elapsed < 0.1  # Should be very fast
```

---

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

---

**Last Updated**: January 2026
