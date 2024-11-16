"use client";

import { useEffect, useState } from "react";
import { FileAudio2 } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { retrieveDatabase } from "../api/getTranscriptions";
import { CustomPagination } from "./CustomPagination";
import "./index.css";

/**
 * Displays paginated transcription records with auto-refresh functionality
 * Fetches and displays transcription records from database on component mount
 * Records are paginated (3 per page) with accordion view for details
 * Displays "No transcripts found" message if database is empty
 */

export default function RecordList() {
  const [records, setRecords] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const recordsPerPage = 3; // Show 3 records per page

  useEffect(() => {
    async function fetchRecords() {
      try {
        const data = await retrieveDatabase();
        setRecords(data.data || []);
      } catch (err) {
        console.error("Error fetching records:", err);
      }
    }

    // Initial fetch
    fetchRecords();

    // Listen for insertedRecord event (fired only when user upload an audio file and the transcrition record is inserted successfully)
    // Use fetchRecord to reload the list showing the latest changes.
    const handleInsertedRecord = () => {
      fetchRecords();
    };
    window.addEventListener("insertedRecord", handleInsertedRecord);

    // Cleanup event listener
    return () => {
      window.removeEventListener("insertedRecord", handleInsertedRecord);
    };
  }, []);

  // Index of last record for pagination (e.g., page 2 * 5 items = index 10)
  const indexOfLastRecord = currentPage * recordsPerPage;

  // Index of first record for pagination (e.g., last index 10 - 5 = index 5)
  const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;

  // Get current page records from array using slice
  const currentRecords = records.slice(indexOfFirstRecord, indexOfLastRecord);

  // Total pages needed (e.g., 13 records ÷ 5 per page = 3 pages)
  const totalPages = Math.ceil(records.length / recordsPerPage);

  return (
    <div className="section">
      <div className="section-header">
        <FileAudio2 size={20} />
        Stored Transcripts
      </div>
      <div className="section-content">
        {currentRecords.length === 0 ? (
          <div className="text-gray-500 p-4 text-center">No records found</div>
        ) : (
          <Accordion type="single" collapsible className="w-full">
            {currentRecords.map((record, index) => (
              <AccordionItem key={record.id} value={`item-${index}`}>
                <AccordionTrigger>{record.file_name}</AccordionTrigger>
                <AccordionContent>
                  {record.transcription || "No content available"}
                  <br />
                  <small>
                    Created at: {record.created_at}
                    <br />
                    Duration: {record.duration}, Channel: {record.channel},
                    Sample Rate: {record.sample_rate}
                  </small>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}

        <CustomPagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  );
}
