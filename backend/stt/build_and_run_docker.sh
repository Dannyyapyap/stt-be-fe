#!/bin/bash

# These copies will be mounted to the container during runtime
# Create logs directory and log.log file if they don't exist
if [ ! -d "logs" ]; then
  mkdir logs
  echo "logs directory created"
fi
if [ ! -f "logs/log.log" ]; then
  touch logs/log.log
  echo "log.log file created"
fi

# Create db directory and transcriptions.db file if they don't exist
if [ ! -d "db" ]; then
  mkdir db
  echo "db directory created"
fi
if [ ! -f "db/transcriptions.db" ]; then
  touch db/transcriptions.db
  echo "transcriptions.db file created"
fi

# Build Docker image and run it as a container
docker compose up --build -d

echo "Docker container start up successfully."