FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY greet/ .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_DB=1

# Expose port 8080
EXPOSE 8080

# Run using gunicorn, better for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "greet:app"] 