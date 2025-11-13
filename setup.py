"""
Setup configuration for cricket-analytics package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="cricket-analytics",
    version="0.1.0",
    author="Cricket Analytics Team",
    description="Data-driven T20 cricket analytics with ML and computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cricket-analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "xgboost>=1.7.0",
        "lightgbm>=3.3.5",
        "catboost>=1.2.0",
        "tensorflow>=2.10.0",
        "torch>=2.0.0",
        "opencv-python>=4.8.0",
        "streamlit>=1.25.0",
        "plotly>=5.14.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cricket-dashboard=dashboards.app:main",
        ],
    },
)
