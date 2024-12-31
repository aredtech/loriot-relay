# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY main.py .

# Expose a port if necessary (not needed for your app since it's outbound WebSocket & Webhook only)
# EXPOSE 8080

# Set the command to run the application
CMD ["python", "main.py"]
