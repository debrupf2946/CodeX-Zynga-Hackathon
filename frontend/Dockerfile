FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Ensure the public directory exists
RUN mkdir -p public

# Environment variables
ENV NODE_ENV=development
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"] 