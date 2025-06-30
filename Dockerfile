# Dockerfile (Combined Frontend & Backend)

# Stage 1: Build the React frontend application
FROM node:18-alpine as frontend-build-stage

WORKDIR /app/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend application code
COPY frontend/ .

# Build the React app for production
# This creates the 'build' directory with static files
RUN npm run build

# Stage 2: Build the Python backend and serve the combined application
FROM python:3.9-slim-buster

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory for the application
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy the backend application code
COPY backend/app.py ./backend/

# Copy the built frontend static files into the backend's static directory
# Flask, by default, looks for static files in a 'static' folder inside the app directory
COPY --from=frontend-build-stage /app/frontend/build ./backend/static

# Copy the frontend's index.html into the backend's templates directory
# Flask, by default, looks for templates in a 'templates' folder inside the app directory
RUN mkdir -p ./backend/templates
COPY --from=frontend-build-stage /app/frontend/build/index.html ./backend/templates/index.html

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask application
# Ensure Flask app.py is correctly configured to serve static files and index.html
CMD ["python", "./backend/app.py"]
