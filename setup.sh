#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
  #pip install --upgrade pip
  #pip install -r requirements.txt
else
  echo "requirements.txt not found. Skipping dependency installation."
fi

echo "Project setup complete!"