# Activate the virtual environment
source venv/bin/activate

# Run the FastAPI application using uvicorn
uvicorn app.main:app --reload