# Makefile for Cricket Analytics Project
# Provides convenient commands for development tasks

.PHONY: help install test test-coverage lint format clean all

# Default target
help:
	@echo "Cricket Analytics - Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo "  make test-fast      - Run tests (skip slow tests)"
	@echo "  make lint           - Run code quality checks"
	@echo "  make format         - Format code with black and isort"
	@echo "  make clean          - Remove generated files"
	@echo "  make process-data   - Process all cricket data"
	@echo "  make notebooks      - Start Jupyter notebook server"
	@echo "  make all            - Run format, lint, and test"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Installation complete"

# Run all tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v
	@echo "✅ Tests complete"

# Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=scripts --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated in htmlcov/"

# Run fast tests (skip slow and network tests)
test-fast:
	@echo "🧪 Running fast tests..."
	pytest tests/ -v -m "not slow and not network"
	@echo "✅ Fast tests complete"

# Run unit tests only
test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/ -v -m unit
	@echo "✅ Unit tests complete"

# Run integration tests only
test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/ -v -m integration
	@echo "✅ Integration tests complete"

# Run linting checks
lint:
	@echo "🔍 Running linting checks..."
	@echo "\n--- Flake8 ---"
	flake8 scripts/ tests/ --max-line-length=100 --exclude=__pycache__
	@echo "\n--- Black (check) ---"
	black --check scripts/ tests/
	@echo "\n--- isort (check) ---"
	isort --check-only scripts/ tests/
	@echo "✅ Linting complete"

# Format code
format:
	@echo "🎨 Formatting code..."
	@echo "\n--- Black ---"
	black scripts/ tests/
	@echo "\n--- isort ---"
	isort scripts/ tests/
	@echo "✅ Code formatting complete"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf dist/ build/
	@echo "✅ Cleanup complete"

# Process cricket data
process-data:
	@echo "⚙️  Processing cricket data..."
	python scripts/process_all_matches.py
	@echo "✅ Data processing complete"

# Start Jupyter notebooks
notebooks:
	@echo "📓 Starting Jupyter notebook server..."
	jupyter notebook

# Download sample data
download-sample:
	@echo "📥 Downloading sample cricket data..."
	python -c "from scripts.cricsheet_downloader import download_cricsheet_data; \
	           download_cricsheet_data('t20_internationals_male', 'data/external')"
	@echo "✅ Download complete"

# Run all quality checks
all: format lint test
	@echo "✅ All checks passed!"

# Development setup (first time)
setup: install
	@echo "🔧 Setting up development environment..."
	@mkdir -p data/external data/processed data/raw
	@echo "✅ Development environment ready"

# Quick validation before commit
pre-commit: format lint test-fast
	@echo "✅ Pre-commit checks passed!"

# CI simulation (runs what CI would run)
ci: lint test-coverage
	@echo "✅ CI simulation complete"
