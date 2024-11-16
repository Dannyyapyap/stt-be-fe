# Speech to Text Frontend Application

## A frontend application built using NextJS v14.2.16 to interface with the [Backend application](https://github.com/Dannyyapyap/stt)

## Pre-requiste

Tested on

Ensure that you have node and npm installed

- node v18.19.1
- npm 9.2.0

## Getting Started

### Running Locally

There are two method for setting up the project locally: using the provided setup script (setup_env.sh) or setting it up manually

---

### Method 1: Setup with the provided script

1.  From the root project directory, run the setup script to automate the environment setup:

    ```bash
    bash setup_env.sh
    ```

    Note: if your backend application is hosted on another port, do make the necessary change in .env.local

### Method 2: Setup Manually

1.  Install dependencies:

    ```bash
    npm install
    ```

    Shadcn UI

    ```bash
    # Only install if there are missing packages from Shadcn
    npx shadcn@latest add accordion
    npx shadcn@latest add button
    npx shadcn@latest add input
    npx shadcn@latest add pagination
    ```

    Note: By default, these components from Shadcn should already be included in the project folder.

2.  Configure environment variables

    create /frontend-ui-stt/.env.local

    ```bash
    NEXT_PUBLIC_API_ENDPOINT=http://localhost:8020
    ```

    Note: This is the endpoint which is hosting your backend application, the backend application has to be running, please refer to
    [stt](https://github.com/Dannyyapyap/stt)

## Run the development server on local:

    ```bash
    npm run dev
    # or
    yarn dev

## Running via Docker

This guide explains how to run the application using Docker.

## Prerequisites

- Docker version 27.3.0 or later (tested with build e85edf8)
- Docker Compose version v2.29.6 or later

## Configuration

Before starting, configure the API endpoint in `build_and_run_docker.sh`:

```bash
API_ENDPOINT="http://172.17.0.1:8020"  # Default Docker internal host, port 8020
```

Replace this value with your STT backend application's hostname and port if different.

## Usage

### Initial Setup and Run

1. Build the Docker image and start the container:
   ```bash
   bash build_and_run_docker.sh
   ```
   By default, the application is served on port 3000. To use a different port, modify the `Dockerfile`.

### Container Management

**View Logs**

```bash
docker compose logs -f
```

**Stop Container**

```bash
docker compose down -v
```

**Restart Container**

```bash
docker compose up -d
```

### Updating Configuration

If you need to change the STT backend application's host:port:

1. Update the `API_ENDPOINT` in `build_and_run_docker.sh`
2. Rebuild and restart the container:
   ```bash
   bash build_and_run_docker.sh
   ```

## To verify that code is running

1.  Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
