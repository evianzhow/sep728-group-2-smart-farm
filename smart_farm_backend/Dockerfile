FROM python:3.11.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the startup script executable
RUN chmod +x startup.sh

# Command to run the startup script
ENTRYPOINT ["/bin/bash"]
CMD ["./startup.sh"]