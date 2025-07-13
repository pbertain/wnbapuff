#!/bin/bash
# Development setup script for WNBA API project

echo "Setting up development environment for WNBA API project..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
if pip install -r requirements.txt; then
    echo "✅ Core dependencies installed successfully"
    echo ""
    echo "💡 To install API server dependencies (optional):"
    echo "  pip install -r requirements-api.txt"
else
    echo "⚠️  First attempt failed, trying minimal requirements..."
    if pip install -r requirements-minimal.txt; then
        echo "✅ Minimal dependencies installed successfully"
        echo ""
        echo "💡 To install API server dependencies (optional):"
        echo "  pip install -r requirements-api.txt"
    else
        echo "❌ Installation failed. Trying individual packages..."
        pip install requests pytz python-dotenv
    fi
fi

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "To test the scripts:"
echo "  python3 wnba_scores.py"
echo "  python3 wnba_standings.py"
echo "  python3 wnba_schedule.py"
echo ""
echo "Don't forget to create a .env file with your API key!"
echo "  touch .env"
echo "  # Then add: SPORTSBLAZE_API_KEY=your_key_here" 