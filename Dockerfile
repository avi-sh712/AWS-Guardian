# Use the "slim" variant to keep the image small (approx. 150MB vs 1GB+)
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# We add 'rm -rf' at the end to keep the layer small
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first
# This leverages Docker caching: if requirements don't change, 
# this step is skipped on re-builds
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces size by not saving the downloaded wheel files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Gradio uses
EXPOSE 7860

# Run the dashboard
CMD ["python", "dashboard.py"]