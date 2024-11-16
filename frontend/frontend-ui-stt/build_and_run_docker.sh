#!/bin/bash

# Define the API endpoint
API_ENDPOINT="http://172.17.0.1:8020"  # Change this value manually when needed

# Export for runtime
export NEXT_PUBLIC_API_ENDPOINT=$API_ENDPOINT

# Build with the argument and start containers
docker compose build --build-arg NEXT_PUBLIC_API_ENDPOINT=$API_ENDPOINT
docker compose up -d

echo "Using API endpoint: $NEXT_PUBLIC_API_ENDPOINT"
echo "Containers are starting..."