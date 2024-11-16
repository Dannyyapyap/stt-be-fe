"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { searchDatabase } from "../api/search";
import { CustomPagination } from "./CustomPagination";
import "./index.css";

/**
 * Keyword search for audio file name and transcription content
 * - Filters records by filename/transcription keyword matches
 * - Paginates results (1 per page)
 * - Shows "No Results found for your search" when no matches
 */

export default function SearchRecord() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 1; // View only 1 result per page

  async function submitQuery() {
    if (!searchQuery) return;

    setIsUploading(true);
    try {
      const result = await searchDatabase(searchQuery);

      if (result && result.record > 0) {
        const uniqueResults = getUniqueResults(result.data); // Send it to getUniqueResults to remove duplicated record.
        setSearchResults(uniqueResults); // Only set the unique results
        setCurrentPage(1); // Reset to first page on new search
      } else {
        setSearchResults([]); // No records found, set empty array
        console.log("No records found.");
      }
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setIsUploading(false);
    }
  }

  // Function to remove duplicates based on transcription content
  function getUniqueResults(data) {
    const seenTranscriptions = new Set(); //Each value in a set is a unique value, effective for filtering duplicate
    const uniqueResults = [];

    // Iterate over the data and add unique transcriptions to the uniqueResults array
    // Check if the transcription has already been encountered
    // `seenTranscriptions.has(transcription)` checks if the transcription is already in the Set
    // The `!` negates the result, so if the transcription is NOT in the Set, it will return `true`
    for (const item of data) {
      const transcription = item.transcription.trim(); // Normalize by trimming whitespaces
      if (!seenTranscriptions.has(transcription)) {
        seenTranscriptions.add(transcription);
        uniqueResults.push(item);
      }
    }

    // Return all the unique results
    return uniqueResults;
  }

  // Custom Pagination calculations
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = searchResults?.slice(
    indexOfFirstResult,
    indexOfLastResult
  );
  const totalPages = searchResults
    ? Math.ceil(searchResults.length / resultsPerPage)
    : 0;

  return (
    <div className="section">
      <div className="section-header">
        <Search size={20} />
        Search records for related content
      </div>
      <div className="section-content">
        <Input
          type="text"
          placeholder="Enter keyword related to filename or transcript content"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="section-action"
        />
        <Button
          onClick={submitQuery}
          disabled={isUploading || !searchQuery}
          className="section-action"
        >
          {isUploading ? "Searching..." : "Search Record"}
        </Button>

        {/* Display error messages when request comes back with an error */}
        {errorMessage && <div className="error">{errorMessage}</div>}

        {/* Display search results or a message if no results are found */}
        {searchResults && searchResults.length > 0 ? (
          <div>
            <strong>Search Result(s):</strong>
            <ul className="search-result-list">
              {currentResults.map((item) => (
                <li key={item.id}>
                  {item.transcription}
                  <br />
                  <small>
                    File Name: {item.file_name}, Channel: {item.channel}, Sample
                    Rate: {item.sample_rate}, Duration: {item.duration}s
                  </small>
                  <br />
                  <small>Created at: {item.created_at}</small>
                </li>
              ))}
            </ul>
            <CustomPagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </div>
        ) : searchResults && searchResults.length === 0 ? (
          <div>No results found for your search.</div>
        ) : null}
      </div>
    </div>
  );
}
