# Use an official Node.js runtime as a parent image
FROM node:16-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./
RUN npm install

# Copy the .env file to the working directory
COPY .env .env

# Copy the rest of the application code to the working directory
COPY . .
# Build the application
RUN npm run build

# Use an official Nginx image to serve the application
FROM nginx:alpine
# Copy the built application from the previous stage to the Nginx HTML directory
COPY --from=build /app/build /usr/share/nginx/html
# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose port 80
EXPOSE 80
# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
