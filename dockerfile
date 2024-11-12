FROM python:3.12

# Set the working directory
WORKDIR /app

# Install Rust using rustup
RUN apt-get update && apt-get install -y curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy the requirements file and install the rest of the dependencies
COPY requirements.txt .

# Install dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy the rest of the application code
COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]