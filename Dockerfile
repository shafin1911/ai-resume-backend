# Use official Python image
FROM python:3.11

# Install system dependencies including psql
RUN apt-get update && apt-get install -y libpq-dev postgresql-client

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
