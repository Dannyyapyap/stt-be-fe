//  Endpoint for retrieving transcription records from database
//  Retrieve the list of record
//  e.g. {"record": 10, "data": [{...}, {...}, ...]

export async function retrieveDatabase() {
  try {
    const response = await fetch(`/data/transcriptions`, {
      method: "GET",
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Request failed with status: ${response.status}, message: ${errorText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to retrieve list of record:", error);
    throw error;
  }
}
