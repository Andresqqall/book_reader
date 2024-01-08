# Use a specific version of Python for Poetry
FROM python:3.12-alpine as python-base

# Install system dependencies for building Python packages
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Install Poetry
ENV POETRY_VERSION=1.7.1
RUN pip install poetry==$POETRY_VERSION

# Set Poetry environment variables
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PYTHONUNBUFFERED=1
ENV PYTHONBURRED=1
# Set the working directory for the app
WORKDIR /opt/book-reader-backend/

# Copy the dependency files
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project configuration

# Install dependencies
RUN poetry install

# Copy the application files
COPY . .

# Expose the port (if needed)
EXPOSE 5000
