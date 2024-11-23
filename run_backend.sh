#!/bin/bash

# Create and run the Docker container in detached mode
docker build -t spending-app-backend .

# Create db file
touch test.db

docker run -d --name spending-app-backend-container \
  -p 8000:8000 \
  -v $(pwd)/test.db:/app/test.db \
  spending-app-backend