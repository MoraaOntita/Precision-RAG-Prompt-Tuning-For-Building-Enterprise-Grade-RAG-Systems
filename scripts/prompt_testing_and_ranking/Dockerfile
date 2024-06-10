# Use a base image with Python installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose the port the app runs on (if applicable)
# EXPOSE 5000  # Uncomment if your service runs on a specific port

# Command to run the application
CMD ["python", "prompt_testing_and_ranking.py"]

