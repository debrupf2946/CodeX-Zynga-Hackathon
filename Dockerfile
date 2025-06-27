FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies with improved error handling for PyTorch
RUN pip install --upgrade pip && \
    # Install PyTorch separately with a specific URL to avoid invalid wheel issues
    pip install --no-cache-dir torch==2.0.0 torchvision==0.15.1 --index-url https://download.pytorch.org/whl/cpu && \
    # Install the rest of the requirements
    pip install --no-cache-dir -r requirements.txt

# Copy model files
COPY models/ /app/models/

# Copy backend code
COPY backend/ /app/

# Create directory for uploaded files
RUN mkdir -p static

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "app:app"] 