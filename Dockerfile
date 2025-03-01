# Use official Python image
FROM python:3.11-slim 

# Install system dependencies including `make`
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev postgresql-client make gcc g++ \
    && rm -rf /var/lib/apt/lists/*  # ✅ Reduce image size

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the project files after installing dependencies
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set environment variables
ENV OPENBLAS_NUM_THREADS=1

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]