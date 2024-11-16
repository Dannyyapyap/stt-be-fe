/**
 * FileUpload Component Test Suite
 *
 * Tests performed:
 * 1. Initial Render: Verifies upload button is disabled by default
 * 2. File Selection: Confirms button enables when valid file is selected
 * 3. Upload Success: Tests successful file upload flow and success message
 *
 * Test setup:
 * - Mocks uploadAudio API from upload.js
 *   - Mocked to return { status: 200 } on success
 *   - Used to simulate file upload operations
 * - Creates mock audio files with type 'audio/mpeg'
 * - Clears mocks before each test
 */

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import FileUpload from "../components/FileUpload";
import { uploadAudio } from "../api/upload";

// Mock the upload API module
jest.mock("../api/upload");

describe("FileUpload Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders upload button in disabled state initially", () => {
    render(<FileUpload />);
    const uploadButton = screen.getByRole("button");
    expect(uploadButton).toBeDisabled();
  });

  test("enables upload button when file is selected", () => {
    render(<FileUpload />);
    const fileInput = screen.getByTestId("file-upload");
    const file = new File(["dummy"], "test.mp3", { type: "audio/mpeg" });

    fireEvent.change(fileInput, { target: { files: [file] } });

    const uploadButton = screen.getByRole("button");
    expect(uploadButton).not.toBeDisabled();
  });

  test("handles successful file upload", async () => {
    uploadAudio.mockResolvedValue({ status: 200 });

    render(<FileUpload />);
    const fileInput = screen.getByTestId("file-upload");
    const file = new File(["dummy"], "test.mp3", { type: "audio/mpeg" });

    // Select and upload file
    fireEvent.change(fileInput, { target: { files: [file] } });
    fireEvent.click(screen.getByRole("button"));

    // Check success message appears
    await waitFor(() => {
      expect(screen.getByText(/successfully uploaded/i)).toBeInTheDocument();
    });
  });
});
