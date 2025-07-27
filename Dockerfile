# Multi-stage build for React app
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY client/package*.json ./client/
COPY server/package*.json ./server/

# Install dependencies
RUN npm install
RUN cd client && npm install
RUN cd server && npm install

# Copy source code
COPY client/ ./client/
COPY server/ ./server/

# Build React app
RUN cd client && npm run build

# Production stage
FROM node:18-alpine

# Create app directory
WORKDIR /app

# Copy server package files and install production dependencies
COPY server/package*.json ./
RUN npm install --only=production

# Copy built React app and server code
COPY --from=build /app/client/build ./public
COPY server/ ./

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3001

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/api/data', (res) => { process.exit(res.statusCode === 401 ? 0 : 1) })"

# Start the application
CMD ["npm", "start"] 