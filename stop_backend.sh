#!/bin/bash

# Stop and remove the Docker container
docker stop spending-app-backend-container

rm test.db

docker rm spending-app-backend-container