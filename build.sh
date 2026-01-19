#!/bin/bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

# Configuration
IMAGE_NAME="asset-agent"
CONTAINER_NAME="asset-agent-app"
PORT=8000

echo "=== Asset Agent Deployment Script ==="
echo ""

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed.${NC}"
        echo "Would you like to install Docker? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            install_docker
        else
            echo -e "${RED}Docker is required. Exiting.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ Docker is installed${NC}"
        docker --version
    fi
}

# Install Docker (supports Ubuntu/Debian and macOS)
install_docker() {
    echo -e "${YELLOW}Installing Docker...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux installation
        sudo apt-get update
        sudo apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release
        
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        
        # Add current user to docker group
        sudo usermod -aG docker "$USER"
        echo -e "${GREEN}Docker installed successfully!${NC}"
        echo -e "${YELLOW}Note: You may need to log out and back in for group changes to take effect.${NC}"
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS installation
        if command -v brew &> /dev/null; then
            brew install --cask docker
            echo -e "${GREEN}Docker installed successfully!${NC}"
            echo -e "${YELLOW}Please start Docker Desktop from Applications.${NC}"
        else
            echo -e "${RED}Homebrew not found. Please install Docker Desktop manually from https://www.docker.com/products/docker-desktop${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Unsupported OS. Please install Docker manually.${NC}"
        exit 1
    fi
}

# Check if OpenAI API key is set
check_api_key() {
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${YELLOW}Warning: OPENAI_API_KEY environment variable is not set.${NC}"
        echo "Please enter your OpenAI API key:"
        read -r -s api_key
        export OPENAI_API_KEY="$api_key"
        echo ""
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}Error: OPENAI_API_KEY is required.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ API key is set${NC}"
}

# Stop and remove existing container
cleanup_existing() {
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${YELLOW}Stopping and removing existing container...${NC}"
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
        echo -e "${GREEN}✓ Cleaned up existing container${NC}"
    fi
}

# Build Docker image
build_image() {
    echo ""
    echo "Building Docker image: $IMAGE_NAME"
    if docker build -t "$IMAGE_NAME" .; then
        echo -e "${GREEN}✓ Image built successfully${NC}"
    else
        echo -e "${RED}Error: Failed to build Docker image${NC}"
        exit 1
    fi
}

# Run Docker container
run_container() {
    echo ""
    echo "Starting container: $CONTAINER_NAME"
    if docker run -d \
        --name "$CONTAINER_NAME" \
        -p $PORT:8000 \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" \
        --restart unless-stopped \
        "$IMAGE_NAME"; then
        echo -e "${GREEN}✓ Container started successfully${NC}"
    else
        echo -e "${RED}Error: Failed to start container${NC}"
        exit 1
    fi
}

# Display status
show_status() {
    echo ""
    echo "=== Deployment Complete ==="
    echo -e "${GREEN}Application is running!${NC}"
    echo ""
    echo "Access the API at: http://localhost:$PORT"
    echo "API documentation: http://localhost:$PORT/docs"
    echo ""
    echo "Useful commands:"
    echo "  View logs:    docker logs $CONTAINER_NAME"
    echo "  Stop app:     docker stop $CONTAINER_NAME"
    echo "  Start app:    docker start $CONTAINER_NAME"
    echo "  Remove app:   docker rm -f $CONTAINER_NAME"
    echo ""
}

# Main execution
main() {
    check_docker
    check_api_key
    cleanup_existing
    build_image
    run_container
    show_status
}

main
