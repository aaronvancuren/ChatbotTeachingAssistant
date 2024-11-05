FROM python:3.12

# Set the working directory
WORKDIR /app

# Update pip to the latest version
RUN pip install --upgrade pip

# Install tiktoken separately
RUN pip install --no-cache-dir tiktoken

# Copy the requirements file and install the rest of the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]