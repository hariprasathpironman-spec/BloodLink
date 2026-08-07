# Stage 1: Build the React frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup the Flask backend
FROM python:3.10-slim
WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from Stage 1
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Ensure instance folder exists for SQLite
RUN mkdir -p /app/backend/instance

# Expose port (Koyeb usually uses 8000 or expects the app to listen on PORT)
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=backend/run.py
ENV PORT=8000

# Run with Gunicorn from the backend directory
WORKDIR /app/backend
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT run:app"]
