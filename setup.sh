#!/bin/bash
# Expense Tracker - Setup Script for Beginners
# This script sets up everything automatically

echo "🚀 Expense Tracker Setup Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    echo "   Download from: https://python.org/downloads"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Generate a secret key
echo "🔑 Generating secret key..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "SECRET_KEY=$SECRET_KEY" > .env

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from app import init_db; init_db()"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 To start the application, run:"
echo "   source venv/bin/activate  # (or venv\Scripts\activate on Windows)"
echo "   python app.py"
echo ""
echo "🌐 Then open: http://localhost:5000"
