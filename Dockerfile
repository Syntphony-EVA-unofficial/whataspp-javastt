# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container to /app
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