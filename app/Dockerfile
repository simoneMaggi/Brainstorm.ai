# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY src/ .


# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD ["python", "entrypoint.py"]