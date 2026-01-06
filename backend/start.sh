#!/bin/bash
# Startup script for backend with virtual environment support

echo "Starting Basil Backend..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "WARNING: No virtual environment found. Using system Python."
    echo "Please create a virtual environment:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
fi

# Run uvicorn
echo "Running uvicorn..."
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
