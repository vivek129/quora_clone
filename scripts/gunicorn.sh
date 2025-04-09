#!/usr/bin/bash

# Replace {YOUR_PROJECT_MAIN_DIR_NAME} with your actual project directory name
PROJECT_MAIN_DIR_NAME="quora_clone"

# Copy gunicorn socket and service files
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/gunicorn/gunicorn.socket" "/etc/systemd/system/quora_clone-gunicorn.socket"
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/gunicorn/gunicorn.service" "/etc/systemd/system/quora_clone-gunicorn.service"

# Start and enable Gunicorn service
sudo systemctl start quora_clone-gunicorn.service
sudo systemctl enable quora_clone-gunicorn.service