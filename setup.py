"""
Setup script for Cricket Analytics project
Makes installation and setup much simpler
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cricket-analytics",
    version="1.0.0",
    author="Aalap Desai",
    author_email="adesai@altsportsdata.com",
    description="Comprehensive cricket analytics platform with data processing, ML, and visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cricket-analytics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cricket-download=scripts.cricsheet_downloader:main",
            "cricket-process=scripts.process_all_matches:main",
        ],
    },
)
