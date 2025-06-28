# Use an official Python runtime as the parent image
FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container to /app
WORKDIR /app

# Install any Python packages specified in requirements.txt
# Copy requirements file
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy the local package directory content into the container at /app
COPY . /app

EXPOSE 31415

# Define any environment variables
# ENV KEY Value

# Print environment variables (for debugging purposes, you can remove this line if not needed)
RUN ["printenv"]

# Run Python script when the container launches, with hot-reloading
CMD watchfiles --filter python "python -u ./runShortGPT.py" "."