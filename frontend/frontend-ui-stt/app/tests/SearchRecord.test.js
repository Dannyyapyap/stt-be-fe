/**
 * SearchRecord Component Test Suite
 *
 * Tests performed:
 * 1. Initial Render: Verifies search input and button are present
 * 2. Search Results: Tests successful search flow and result display
 * 3. Empty Results: Validates "no results" message for unsuccessful searches
 *
 * Mock data structure:
 * - Audio records with:
 *   - Metadata (filename, format, sample rate)
 *   - Transcription content
 *   - Timestamps
 *
 * Test setup:
 * - Mocks searchDatabase API from search.js
 * - Uses waitFor for async operations
 * - Clears mocks before each test
 */

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import SearchRecord from "../components/SearchRecord";
import { searchDatabase } from "../api/search";

// Mock the search API module
jest.mock("../api/search");

describe("SearchRecord Component", () => {
  const mockRecords = {
    record: 2,
    data: [
      {
        id: 1,
        file_name: "sample.mp3",
        audio_format: "mp3",
        channel: 1,
        sample_rate: 48000,
        transcription: "sample content that is being tested welcome",
        created_at: "2024-11-14 18:05:41",
      },
      {
        id: 2,
        file_name: "sample2.mp3",
        audio_format: "mp3",
        channel: 1,
        sample_rate: 41600,
        transcription: "second content that is being tested goodbye",
        created_at: "2024-12-12 15:12:42",
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders search interface correctly", () => {
    render(<SearchRecord />);

    expect(screen.getByPlaceholderText(/Enter keyword/)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Search Record/i })
    ).toBeInTheDocument();
  });

  test("performs search and displays results", async () => {
    searchDatabase.mockResolvedValueOnce(mockRecords);

    render(<SearchRecord />);

    // Perform search
    const input = screen.getByPlaceholderText(/Enter keyword/);
    const button = screen.getByRole("button", { name: /Search Record/i });

    fireEvent.change(input, { target: { value: "test" } });
    fireEvent.click(button);

    // Verify first result is displayed
    await waitFor(() => {
      expect(
        screen.getByText("sample content that is being tested welcome")
      ).toBeInTheDocument();
      expect(screen.getByText(/File Name: sample.mp3/)).toBeInTheDocument();
      expect(screen.getByText(/Sample Rate: 48000/)).toBeInTheDocument();
    });
  });

  test("handles empty search results", async () => {
    searchDatabase.mockResolvedValueOnce({ record: 0, data: [] });

    render(<SearchRecord />);

    const input = screen.getByPlaceholderText(/Enter keyword/);
    const button = screen.getByRole("button", { name: /Search Record/i });

    fireEvent.change(input, { target: { value: "nonexistent" } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(
        screen.getByText("No results found for your search.")
      ).toBeInTheDocument();
    });
  });
});
