# Speech to Text Service

A FastAPI service that transcribes audio files using OpenAI's Whisper model via HuggingFace's Inference API.

## Pre-requisite

Tested on

- Python Version: 3.12.3
- OS: Ubuntu 24.04

1. Install FFMPEG (for audio processing)

   - For Ubuntu:

   ```bash
   sudo apt install ffmpeg
   ```

   - For other OS, please refer to [FFMPEG Download](https://www.ffmpeg.org/download.html)

2. Ensure application has internet connection

3. Ensure that you have created your HuggingFace API Token, please refer to [Serverless Infernce API](https://huggingface.co/docs/api-inference/en/index)

## Getting Started

### Running Locally

There are two methods for setting up the project locally: using the provided setup script (setup_env.sh) or setting it up manually

---

### Method 1: Setup with the provided script

1.  From the root project directory, run the setup script to automate the environment setup:

    ```bash
    bash setup_env.sh
    ```

2.  Once the script finish running, activate the virtual environment:

    ```bash
    source env/bin/activate   # For Linux/Mac
    # or
    .\env\Scripts\activate    # For Windows
    ```

3.  Replace `your_hugging_face_api_token_here` in the .env file with your actual HuggingFace API token

### Method 2: Setup manually

1. Create and activate Python virtual environment

   ```bash
   # Create virtual environment
   python3 -m venv env

   # Activate environment
   source env/bin/activate   # For Linux/Mac
   # or
   .\env\Scripts\activate    # For Windows
   ```

   Note: Requires Python 3.12.3 or above

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables

   Create `/stt/.env` file with the following content:

   ```env
   WHISPER_MODEL=openai/whisper-tiny
   HF_TOKEN=your_hugging_face_api_token_here
   HF_MAX_RETRIES=5
   HF_RETRY_DELAY=2
   ```

   Note: Replace `your_hugging_face_api_token_here` with your actual HuggingFace API token

### Running the code

By running the below command, the application will be served on port 8020. Feel free to change the port if necessary

For running in development mode:

```
fastapi dev --port 8020
```

For running in production mode:

```
fastapi run --port 8020
```

### Running via Docker

Tested on
Docker version 27.3.0, build e85edf8
Docker Compose version v2.29.6

1. Replace `<INPUT YOU HUGGINGFACE API TOKEN HERE>` in the docker-compose.yml with your actual HuggingFace API token

2. Build the Docker image and start it in a container, use:

   ```
   bash build_and_run_docker.sh
   ```

   Note: Only run this script on the first setup, if encounter any issues/errors, remove the /db and /logs folder from the directory and re-execute the script.

   After executing the above command, two directories will be created in the location where the docker-compose file is located:

   1. db
   2. logs

3. View the logs of the running container

   ```
   docker compose logs -f
   ```

4. To bring down the container
   ```bash
   docker compose down -v
   ```
5. To bring up the container again

   ```bash
   docker compose up -d

   # If your /db and /logs folder were deleted, re-execute the below command again
   bash build_and_run_docker.sh
   ```

### Accessing the SwaggerUI to verify that code is working

If hosted on port 8020,
access via:

```
localhost:8020/docs
```

## Assumptions

1. No infrastructure to host Whisper model locally, hence using Hugging Face's Inference API

2. Code runs on CPU-only server (no GPU packages installed)

3. Audio content is single channel and not based on dual channel(e.g., Call center recordings, YouTube clips) which might require more preprocessing steps (e.g., downmixing, channel separation)

4. This setup is intended only for prototyping, to test the accuracy and speed of different Whisper models (such as Whisper Tiny, Base, etc.). It is not meant for production use, and as such, the testing will focus on evaluating how the model performs in terms of transcription quality and inference time.

5. There is a limited number of API requests available due to Hugging Face's rate limiting and possibly restricted quotas. In addition, there are restrictions on audio clip duration and file size, with Hugging Face's API typically allowing up to 100MB per file and duration constraints based on the file type and size. For large audio files, splitting them into smaller segments may be necessary.

## Implementation

1. Model Selection:

   - Users can select different Whisper models via `WHISPER_MODEL` environment variable
   - Available models list: [Whisper Models](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)
   - User can specify the VAD aggressiveness via the environment variable "VAD_THRESHOLD", it will be defaulted to 0.3. Least Aggressive: 0.3 to Aggressive: 0.8

2. Model Warm-up:

   - FastAPI application sends initial request at startup
   - Prevents cold start issues for first transcription request

3. Audio Processing:

   - Converts uploads to WAV format (uncompressed)
   - Standardizes to single channel
   - Resamples to 16kHz for optimal accuracy

4. Voice Detection:

   - Uses VAD (Voice Activity Detection) to remove silences
   - Improves accuracy and reduces resource usage

5. Transcription

   - Uses the selected model, the processed audio chunks are sent for transcription

6. Data storage
   - The transcript together with the audio metadata will be saved into the SQLite DB
   - Users can retrieve the list of stored transcription records.
   - Users can search for records using partial strings (file names or transcriptions). The search is case-insensitive.
   - Users will be able to delete record based on their record ID.

## Huggingface Resource

- Base model used: [whisper-tiny](https://huggingface.co/openai/whisper-tiny)
- Other available models: [Whisper Models](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)
