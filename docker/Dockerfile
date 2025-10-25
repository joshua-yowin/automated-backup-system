# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster as builder

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcl-dev \
    tk-dev \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a new stage for the final image
FROM python:3.9-slim-buster

# Install system dependencies for tkinter (runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcl \
    tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the rest of the application code
COPY . .

# Make port 5000 available to the world outside this container (for web dashboard)
EXPOSE 5000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden by docker-compose)
CMD ["python3", "dashboard/gui_enhanced.py"]