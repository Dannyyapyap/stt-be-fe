# Speech to Text Transcription Frontend UI Testing

## Overview

This repository contains comprehensive test suites for our Speech-to-Text (STT) transcription Frontend UI, using React Testing Library to ensure reliable component functionality and user interactions.

## Test Categories

### Component Unit Tests

#### 1. FileUpload Component Tests

- **Objective:** Verify file upload functionality and user feedback
- **Coverage:**
  - Initial render state validation
  - File selection behavior
  - Upload success/failure handling
- **API Mocked:** `uploadAudio` from '../api/upload'

#### 2. RecordList Component Tests

- **Objective:** Validate transcription record display
- **Coverage:**
  - Record list rendering
  - Empty state handling
  - Transcription text display
- **API Mocked:** `retrieveDatabase` from '../api/getTranscriptions'

#### 3. SearchRecord Component Tests

- **Objective:** Test search functionality
- **Coverage:**
  - Search interface rendering
  - Results display
  - Empty results handling
- **API Mocked:** `searchDatabase` from '../api/search'

## Setup and Execution

### Prerequisites

1. Install dependencies:

```bash
npm install
# Test-specific dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## Test Structure

```
src/
├── components/
│   ├── FileUpload.js
│   ├── RecordList.js
│   └── SearchRecord.js
├── tests/
│   ├── FileUpload.test.js
│   ├── RecordList.test.js
│   └── SearchRecord.test.js
│   └── audio/sample.mp3
└── api/
    ├── upload.js
    ├── getTranscriptions.js
    └── search.js
```

## Component Test Details

### FileUpload Component

- Tests button disable/enable states
- Validates file selection behavior
- Verifies upload success messages
- Uses mock audio file with type 'audio/mpeg'

### RecordList Component

- Tests record display with mock transcription data
- Validates empty state messaging
- Verifies transcription text display
- Mock data structure: { data: [...records] }

### SearchRecord Component

- Tests search input and button rendering
- Validates search results display
- Verifies "no results found" messaging
- Mock data: Search results with transcription records
