# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependency files and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and Stockfish binary
COPY ./backend /app/backend
COPY ./stockfish_binary /app/stockfish_binary

# Make the Stockfish binary executable
RUN chmod +x /app/stockfish_binary/stockfish

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]