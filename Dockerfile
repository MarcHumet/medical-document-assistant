# Dockerfile for Medical Document Assistant
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to disable langsmith
ENV LANGCHAIN_TRACING_V2=false
ENV LANGCHAIN_ENDPOINT=""
ENV LANGCHAIN_API_KEY=""

# Copy source code
COPY . .

# Create logs directory for loguru
RUN mkdir -p /app/logs

# Create uploads directory
RUN mkdir -p uploads

# Create non-root user for security
RUN addgroup --system --gid 1001 appuser \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser

# Change ownership of app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8000 8501

# Command will be specified in docker-compose.yml