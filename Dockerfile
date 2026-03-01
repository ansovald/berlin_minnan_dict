# Stage 1: Build the React frontend
FROM node:25-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY dictionary-frontend/package*.json ./
RUN npm install

# Copy frontend source and build
COPY dictionary-frontend/ ./
RUN npm run build

# Stage 2: Final image with both backend and frontend
FROM python:3.12-slim

# Install nginx and supervisor
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for backend
WORKDIR /app/backend

# Copy backend requirements and install dependencies
COPY dictionary-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY dictionary-backend/ .

# Copy built frontend from build stage
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 80
EXPOSE 80

# Start supervisor to manage both nginx and Flask
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
