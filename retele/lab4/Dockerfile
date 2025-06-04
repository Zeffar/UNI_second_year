FROM python:3-slim

# Install curl
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Flask
RUN pip install flask

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run Flask application
CMD ["python", "app.py"]