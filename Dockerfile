# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Set the TRANSFORMERS_CACHE environment variable
ENV TRANSFORMERS_CACHE=/tmp/.cache/huggingface

# Create the cache folder with appropriate permissions
RUN mkdir -p $TRANSFORMERS_CACHE && chmod -R 777 $TRANSFORMERS_CACHE

# Set NLTK data directory
ENV NLTK_DATA=/tmp/nltk_data

# Create the NLTK data directory with appropriate permissions
RUN mkdir -p $NLTK_DATA && chmod -R 777 $NLTK_DATA

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 7860

# Run the application.
CMD uvicorn 'main:app' --host=0.0.0.0 --port=7860 