FROM node:22-slim

# Install OpenClaw
RUN npm install -g openclaw

# Create workspace
WORKDIR /workspace

# Copy project files
COPY . .

# OpenClaw gateway port
EXPOSE 3007

# Start OpenClaw gateway
CMD ["openclaw", "gateway", "start", "--foreground"]
