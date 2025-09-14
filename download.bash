#!/bin/bash

# Step 1: Pull the latest Selenium Chrome Docker image
docker pull selenium/standalone-chrome:latest

# Step 2: Run the container in detached mode with port mapping
docker run -d --name my-proxy -p 6767:6767 selenium/standalone-chrome:latest tail -f /dev/null

# Step 3: Install Python, pip, Flask, and Selenium inside the container
docker exec -it my-proxy bash -c "apt update && apt install -y python3 python3-pip && pip3 install flask selenium"

# Step 4: Create a simple Flask app inside the container
docker exec -it my-proxy bash -c "echo \"from flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello from Flask inside Docker!'\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=6767)\" > /app.py"

# Step 5: Run the Flask app inside the container
docker exec -d my-proxy python3 /app.py

echo "Setup complete! Flask app is running at http://localhost:6767"
