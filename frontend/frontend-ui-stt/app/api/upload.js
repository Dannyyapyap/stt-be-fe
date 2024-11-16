// API Endpoint to interface with the stt-api deployed.
// 1) Send audio file as a request for transcription

export async function uploadAudio(audio) {
  const formData = new FormData();
  formData.append("audio", audio);

  // Using Proxy URL set in next.config.mjs to bypass CORS issue
  try {
    const response = await fetch("/stt/transcribe", {
      method: "POST",
      body: formData,
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Upload failed with status: ${response.status}, message: ${errorText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
}
