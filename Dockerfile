# FinOps Bot - Cloud Cost Optimizer
# Dockerfile for containerizing the Python cost optimization script
# Author: Deniz
# Usage: docker build -t finops-bot . && docker run finops-bot

# Use official Python slim image for smaller footprint
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="Deniz"
LABEL description="Cloud Cost Optimization Tool - DevOps Portfolio Project"
LABEL version="1.0"

# Set working directory inside container
WORKDIR /app

# Set environment variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal (unbuffered)
ENV PYTHONUNBUFFERED=1

# Copy application files into container
COPY cloud_inventory.json .
COPY cloud_cost_optimizer.py .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import json; json.load(open('cloud_inventory.json'))" || exit 1

# Default command - run the cost optimizer in auto mode
CMD ["python", "cloud_cost_optimizer.py", "--auto"]
