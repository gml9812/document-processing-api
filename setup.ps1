# Check if virtual environment exists, if not create it
if (-not (Test-Path -Path "venv")) {
  Write-Host "Creating virtual environment..."
  python -m venv venv
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
. venv/Scripts/Activate.ps1

# Install dependencies from requirements.txt
if (Test-Path -Path "requirements.txt") {
  Write-Host "Installing dependencies from requirements.txt..."
  #python -m pip install --upgrade pip
  #pip install -r requirements.txt
  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
} else {
  Write-Host "requirements.txt not found. Skipping dependency installation."
}

Write-Host "Project setup complete!"