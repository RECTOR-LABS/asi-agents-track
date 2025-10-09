#!/bin/bash

# ASI Agents Track - Quick Setup Script

echo "=================================="
echo "ASI Agents Track - Quick Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your Agentverse API keys!"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory created"
echo ""

# Display next steps
echo "=================================="
echo "Setup Complete! 🎉"
echo "=================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Edit .env file with your configuration:"
echo "   nano .env"
echo ""
echo "2. Get your Agentverse API key from:"
echo "   https://agentverse.ai/"
echo ""
echo "3. Review the hackathon requirements:"
echo "   cat TRACK-REQUIREMENTS.md"
echo ""
echo "4. Check the development timeline:"
echo "   cat TIMELINE.md"
echo ""
echo "5. Read the strategic analysis:"
echo "   cat hackathon-analysis.md"
echo ""
echo "6. Start the coordinator agent:"
echo "   python src/agents/coordinator.py"
echo ""
echo "=================================="
echo "Bismillah! Happy Hacking! 🚀"
echo "=================================="
