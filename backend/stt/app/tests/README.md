# Speech to Text Transcription Service Testing

## Overview

This repository contains comprehensive test suites for our Speech-to-Text (STT) transcription service, including both unit and integration tests to ensure reliable functionality and accurate transcriptions.

## Test Categories

### Integration Tests

#### STT Transcription Service Integration Test

These tests verify the end-to-end functionality of the transcription service.

**Key Test Areas:**
- API Connectivity
  - Validates successful connection to Whisper API via HuggingFace
  - Ensures proper API response handling
- Transcription Accuracy
  - Measures Word Error Rate (WER) against reference texts
  - Enforces minimum accuracy thresholds
- Audio Processing Pipeline
  - Validates audio format conversion
  - Tests Voice Activity Detection (VAD) functionality

### Unit Tests

#### 1. Application Status Tests
- **Objective:** Verify application operational status
- **Coverage:** Basic health checks and endpoint availability

#### 2. SQLite Data Pipeline Tests
- **Objective:** Validate database operations for transcription records
- **Test Cases:**
  - Record retrieval functionality
  - Empty result handling
  - Keyword search capabilities
  - Data persistence verification

#### 3. STT Pipeline Component Tests
- **Objective:** Verify individual service components
- **Components Tested:**
  - `AudioReader`: Audio metadata extraction
  - `AudioService`: Format conversion and preprocessing
  - `VADService`: Silence removal and chunking
  - `TranscriptionService`: API integration
  - `SQLiteService`: Database operations

## Setup and Execution

### Prerequisites

1. Complete the main project setup as detailed in [Getting Started](../../README.md)
2. Install test dependencies:
   ```bash
   pip install -r app/tests/requirements.txt
   ```
   Note: Execute the command above from project root directory, ensure that you have already activated the virtual environment containing all dependencies from the project.

### Running Tests

Execute from the project root directory:

```bash
# Run unit tests
pytest app/tests/unit -v -s

# Run integration tests
pytest app/tests/integration -v -s
```

### Test Coverage

Generate and view test coverage reports

Generate coverage reports by running:
```bash
# Generate terminal coverage report for unit tests
pytest --cov=app app/tests/unit -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html app/tests/unit -v
```

```bash
# Generate terminal coverage report for integration tests
pytest --cov=app app/tests/integration -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html app/tests/integration -v
```

The HTML report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in your browser.


## Test Structure

```
app/tests/
├── integration/
│   └── test_transcribe_wer.py
├── unit/
│   ├── test_health.py
│   ├── test_search.py
│   └── test_transcribe.py
└── requirements.txt
```

## Notes

- Tests require a working internet connection for API integration
- Some tests may take longer due to audio processing
- Failed tests will provide detailed error messages for debugging