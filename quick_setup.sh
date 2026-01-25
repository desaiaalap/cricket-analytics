#!/bin/bash
# Quick Setup Script for Cricket Analytics
# Run this to get started in one command!

set -e  # Exit on error

echo "🏏 Cricket Analytics - Quick Setup"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "   ✅ Dependencies installed"
echo ""

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/external data/processed data/raw
echo "   ✅ Directories created"
echo ""

# Ask if user wants to download sample data
echo "📥 Download sample data? (y/n)"
read -r download_data

if [ "$download_data" = "y" ] || [ "$download_data" = "Y" ]; then
    echo "   Downloading T20 World Cup data..."
    python3 << 'EOF'
from scripts.cricsheet_downloader import download_cricsheet_data
try:
    download_cricsheet_data('t20_internationals_male', 'data/external')
    print("   ✅ Data downloaded successfully")
except Exception as e:
    print(f"   ⚠️  Download failed: {e}")
    print("   You can download manually later")
EOF
    echo ""

    # Process data
    echo "⚙️  Processing matches..."
    python3 scripts/process_all_matches.py
    echo "   ✅ Data processed"
    echo ""
fi

echo "✅ Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "   1. Open Jupyter notebooks:    jupyter notebook"
echo "   2. View processed data:       ls data/processed/"
echo "   3. Read the docs:             cat QUICKSTART.md"
echo ""
echo "📊 Quick analysis:"
echo "   python3 -c \"import pandas as pd; print(pd.read_csv('data/processed/player_batting_stats.csv').nlargest(5, 'runs')[['player', 'runs']])\""
echo ""
echo "Happy analyzing! 🚀"
