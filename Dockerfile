# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        libssl-dev \
        libffi-dev \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



# Set working directory
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi redis dramatiq requests 'dramatiq[redis]'



# Copy application code
COPY ./timer_app /app

# Expose the port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "timer:app", "--host", "0.0.0.0", "--port", "8000"]
