// API Endpoint to interface with the search API
//  1) Send search query to the database
//  Retrieve a list of matching record
//  e.g. {"record": 10, "data": [{...}, {...}, ...]

export async function searchDatabase(query) {
  try {
    //encodeURIComponent to handle special character (e.g. $ #) to prevent breaking the URL structure
    const response = await fetch(
      `/data/search?keyword=${encodeURIComponent(query)}`,
      {
        method: "GET",
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Search failed with status: ${response.status}, message: ${errorText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Search error:", error);
    throw error;
  }
}
