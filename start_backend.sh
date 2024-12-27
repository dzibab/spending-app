#!/bin/bash

CONTAINER_NAME="spending-app-backend-container"

# Check if the Docker container is running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  # Stop and remove the container if it is running
  ./stop_backend.sh
fi

# Create and run the Docker container in detached mode
docker build -t spending-app-backend .

# Create db file
touch test.db

docker run -d --name $CONTAINER_NAME \
  -p 8000:8000 \
  -v $(pwd)/test.db:/app/test.db \
  spending-app-backend