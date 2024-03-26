# Set the base image to use for subsequent instructions
# FROM python:3.10-alpine
FROM python:3.9-alpine

# Set the working directory for any subsequent ADD, COPY, CMD, ENTRYPOINT,
# or RUN instructions that follow it in the Dockerfile
WORKDIR /app

# Copy files or folders from source to the dest path in the image's filesystem.
COPY requirements.txt .

# Execute any commands on top of the current image as a new layer and commit the results.
RUN pip install --no-cache-dir -r requirements.txt

# Copy files or folders from source to the dest path in the image's filesystem.
COPY . .

# Set a non-root user to run the container
USER nobody

# Health check to verify the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:5000/ || exit 1

# Configure the container to be run as an executable.
CMD ["python", "app.py"]