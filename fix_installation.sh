#!/bin/bash
# Fix installation issues with WNBA API project

echo "🔧 Fixing installation issues..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Remove any cached files
echo "Cleaning up cached files..."
rm -rf __pycache__
find . -name "*.pyc" -delete

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Try installing with updated requirements
echo "Installing dependencies with updated versions..."
if pip install -r requirements.txt; then
    echo "✅ Installation successful with requirements.txt"
    echo ""
    echo "💡 To install API server dependencies (optional):"
    echo "  pip install -r requirements-api.txt"
elif pip install -r requirements-minimal.txt; then
    echo "✅ Installation successful with minimal requirements"
    echo ""
    echo "💡 To install API server dependencies (optional):"
    echo "  pip install -r requirements-api.txt"
else
    echo "⚠️  Trying individual package installation..."
    pip install requests pytz python-dotenv
fi

echo ""
echo "🎉 Installation fix complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To test the setup:"
echo "  python3 test_setup.py" 