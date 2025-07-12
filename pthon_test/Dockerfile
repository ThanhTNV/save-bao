FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for OpenCV and Tesseract
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install pip packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the test script and the image into the container
COPY test_ocr.py .
COPY test_ocr.jpg .

# Command to run the test script
CMD ["python", "test_ocr.py"] 