# Use an official Python runtime as a parent image
FROM python:3.11.6-bullseye

# Set the working directory in the container
WORKDIR /app

# Apt requirements
RUN apt update && apt install -y ffmpeg

# Copy just requirements to build dependencies 
COPY requirements.txt .

# Install the dependencies
RUN pip install -U pip wheel && \
  pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the API
CMD exec gunicorn -k uvicorn.workers.UvicornWorker --workers 3 --timeout 0 api:app
