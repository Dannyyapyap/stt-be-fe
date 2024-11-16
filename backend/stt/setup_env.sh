#!/bin/bash

# Exit on error
set -e

# Create the virtual environment
python3 -m venv env

# Detect operating system
OS_TYPE=$(uname)

# Platform-specific activation commands
if [[ "$OS_TYPE" == "Darwin" || "$OS_TYPE" == "Linux" ]]; then
    # For Linux or macOS
    echo "Detected Linux or macOS, activating virtual environment..."
    source env/bin/activate
elif [[ "$OS_TYPE" == "CYGWIN"* || "$OS_TYPE" == "MINGW"* || "$OS_TYPE" == "MSYS"* ]]; then
    # For Windows (Git Bash, Cygwin, MSYS)
    echo "Detected Windows, activating virtual environment..."
    source env/Scripts/activate
else
    echo "Unsupported operating system."
    exit 1
fi

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment setup complete and dependencies installed."

# Create .env file with the specified content
cat <<EOL > .env
WHISPER_MODEL=openai/whisper-tiny
HF_TOKEN=your_hugging_face_api_token_here
HF_MAX_RETRIES=5
HF_RETRY_DELAY=2
VAD_THRESHOLD=0.3
EOL

echo ".env file created with necessary configuration."

# Automatically source the virtual environment in the current shell
echo "To activate the virtual environment, run: 'source env/bin/activate' (Linux/macOS) or 'env\\Scripts\\activate' (Windows)"
