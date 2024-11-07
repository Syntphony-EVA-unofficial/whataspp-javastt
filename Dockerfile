# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Add /app to the PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Run main.py when the container launches
CMD uvicorn mainlocal:app --host 0.0.0.0 --port ${PORT:-8080}