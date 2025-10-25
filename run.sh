#!/bin/bash

# This script starts the backup system's GUI dashboard.

# Set the project's root directory
PROJECT_ROOT=$(dirname "$0")

# Ensure the virtual environment is set up and activated
if [ ! -d "$PROJECT_ROOT/venv" ]; then
  python3 -m venv "$PROJECT_ROOT/venv"
  source "$PROJECT_ROOT/venv/bin/activate"
  pip install -r "$PROJECT_ROOT/requirements.txt"
else
  source "$PROJECT_ROOT/venv/bin/activate"
fi

# Run the main application
python3 "$PROJECT_ROOT/dashboard/gui.py"
