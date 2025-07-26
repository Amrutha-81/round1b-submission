# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Run main.py
CMD ["python", "app/main.py"]
