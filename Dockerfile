# Use the official Python lightweight image (not Lambda)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed) and uv
RUN pip install uv

# Copy dependency files first (for caching)
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application
COPY agent/ ./agent/
COPY dashboard.py .
# We don't need lambda_function.py anymore for this deployment

# Expose Gradio's port
EXPOSE 7860

# Set the command to run the dashboard
# host="0.0.0.0" is CRITICAL for running inside Docker
CMD ["python", "dashboard.py"]