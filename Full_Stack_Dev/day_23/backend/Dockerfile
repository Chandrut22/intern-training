# Base image
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first (better Docker cache)
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen

# Copy the rest of the project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]