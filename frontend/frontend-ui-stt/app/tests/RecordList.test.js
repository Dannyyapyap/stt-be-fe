/**
 * RecordList Component Test Suite
 *
 * Tests performed:
 * 1. Record Display: Verifies records are displayed after loading
 * 2. Empty State: Shows appropriate message when no records exist
 * 3. Content Verification: Ensures all record details are shown correctly
 *
 * Test setup:
 * - Mocks retrieveDatabase API from getTranscriptions.js
 * - Uses mock transcription records
 * - Handles async data loading
 */

import { render, screen, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";
import RecordList from "../components/RecordList";
import { retrieveDatabase } from "../api/getTranscriptions";

// Mock the getTranscriptions API
jest.mock("../api/getTranscriptions");

describe("RecordList Component", () => {
  const mockRecords = {
    data: [
      {
        id: 1,
        file_name: "sample.mp3",
        audio_format: "mp3",
        channel: 1,
        sample_rate: 48000,
        transcription: "sample content that is being tested welcome",
        created_at: "2024-11-14 18:05:41",
        duration: "00:30",
      },
      {
        id: 2,
        file_name: "sample2.mp3",
        audio_format: "mp3",
        channel: 1,
        sample_rate: 41600,
        transcription: "second content that is being tested goodbye",
        created_at: "2024-12-12 15:12:42",
        duration: "00:45",
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders record list correctly", async () => {
    // Setup mock
    retrieveDatabase.mockResolvedValue(mockRecords);

    render(<RecordList />);

    // Wait for data to load and check content
    await waitFor(() => {
      expect(screen.getByText("sample.mp3")).toBeInTheDocument();
    });

    // Wrap accordion click in act, click to reveal content
    await act(async () => {
      const accordionTrigger = screen.getByText("sample.mp3");
      accordionTrigger.click();
    });

    // Check content after accordion is opened
    expect(
      screen.getByText(/sample content that is being tested welcome/i)
    ).toBeInTheDocument();
    expect(screen.getByText(/Sample Rate: 48000/i)).toBeInTheDocument();
  });

  test('displays "No records found" when list is empty', async () => {
    // Mock empty response
    retrieveDatabase.mockResolvedValue({ data: [] });

    render(<RecordList />);

    await waitFor(() => {
      expect(screen.getByText(/no records found/i)).toBeInTheDocument();
    });
  });

  test("displays transcription text when accordion is opened", async () => {
    retrieveDatabase.mockResolvedValue(mockRecords);

    render(<RecordList />);

    // Wait for records to load
    await waitFor(() => {
      expect(screen.getByText("sample2.mp3")).toBeInTheDocument();
    });

    // Wrap accordion click in act, click to reveal content
    await act(async () => {
      const accordionTrigger = screen.getByText("sample2.mp3");
      accordionTrigger.click();
    });

    // Check content after accordion is opened
    expect(
      screen.getByText(/second content that is being tested goodbye/i)
    ).toBeInTheDocument();
    expect(screen.getByText(/Sample Rate: 41600/i)).toBeInTheDocument();
  });
});
