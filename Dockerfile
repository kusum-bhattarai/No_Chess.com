# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Stockfish from the official Debian repository
RUN apt-get update && apt-get install -y stockfish

# Add the directory containing the stockfish executable to the system's PATH
ENV PATH="${PATH}:/usr/games"

# Copy dependency files and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./backend /app/backend

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]