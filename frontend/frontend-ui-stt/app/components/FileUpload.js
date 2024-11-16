"use client";

import { useState } from "react";
import { Upload } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { uploadAudio } from "../api/upload";
import "./index.css";

/**
 * Audio file upload and transcription handler
 * - Supports single/multi file uploads
 * - Tracks transcription status via status counter
 * - send 'insertedRecord' event on successful transcription
 * - Event triggers UI refresh in RecordList.js
 */

export default function FileUpload() {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResults, setUploadResults] = useState(null);

  function handleFileSelect(e) {
    setSelectedFiles(e.target.files);
    setUploadResults(null);
  }

  async function handleUpload() {
    if (!selectedFiles?.length) return;

    setIsUploading(true);
    setUploadResults(null);

    try {
      const files = Array.from(selectedFiles);
      const results = { 200: 0, 404: 0, 500: 0 }; // Create an initial count for each of the status

      const uploadPromises = files.map(async (file) => {
        try {
          await uploadAudio(file);
          results[200] = (results[200] || 0) + 1; // When request comes back with status 200, add 1 to the count
        } catch (error) {
          results[500] = (results[500] || 0) + 1; // When request comes back with status 500, add 1 to the count
        }
      });

      await Promise.all(uploadPromises); // This is to allow concurrent upload of multiple files. Requests will be concurrent instead of sequential
      setUploadResults(results);
      window.dispatchEvent(new Event("insertedRecord")); // Send event to trigger reloading of the Stored Transcript record
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      // Clear file upload memory and reset the file input field after all requests have been fulfilled
      setSelectedFiles(null);
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = ""; // Reset the file input field

      setIsUploading(false); // Stop uploading indicator
    }
  }

  function renderStatusMessages() {
    if (!uploadResults) return null;

    const statusMessages = {
      200: "successfully uploaded and transcribed",
      404: "failed to upload",
      500: "encountered server errors, please try again",
    };

    // Access the object of results to obtain the key and the value
    return (
      <div className="status-message">
        {Object.entries(uploadResults).map(
          ([status, count]) =>
            count > 0 && (
              <p key={status}>
                {count} audio file(s){" "}
                {statusMessages[status] || "Unknown status"}.
              </p>
            )
        )}
      </div>
    );
  }

  return (
    <div className="section">
      <div className="section-header">
        <Upload size={20} />
        Upload Audio Files
      </div>
      <div className="section-content">
        <Input
          type="file"
          accept="audio/*"
          multiple
          onChange={handleFileSelect}
          className="section-action"
          data-testid="file-upload"
        />

        {renderStatusMessages()}

        <Button
          onClick={handleUpload}
          disabled={isUploading || !selectedFiles?.length}
          className="section-action"
        >
          {isUploading ? "Uploading..." : "Upload Files"}
        </Button>
      </div>
    </div>
  );
}
