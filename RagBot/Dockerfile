# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system packages (optional, but often needed for some Python deps)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "index8.py", "--server.port=8501", "--server.address=0.0.0.0"]
