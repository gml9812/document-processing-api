# Activate the virtual environment
. venv/Scripts/Activate.ps1

# Run the FastAPI application using uvicorn
python -m uvicorn app.main:app --reload