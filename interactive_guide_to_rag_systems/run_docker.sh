#!/bin/bash
# Build the Docker image
docker build -t interactive_guide_to_rag_systems .

# Run the Docker container, mapping port 8080 on the host to port 80 in the container
docker run -d -p 3200:80 --name interactive_guide_to_rag_systems interactive_guide_to_rag_systems

echo "Web page is now available at http://localhost:8080"

