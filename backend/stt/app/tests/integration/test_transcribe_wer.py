"""
Integration test for the STT transcription service. This test verifies:
1. Successful connection to Whisper API via HuggingFace
2. Accuracy of transcription against a known reference text using Word Error Rate (WER). Accuracy must be above a certain threshold before it is considered "pass"
3. Audio preprocessing pipeline functionality (format conversion, VAD)
"""

from fastapi.testclient import TestClient
from main import app
import os
from jiwer import wer

client = TestClient(app)

def test_transcribe_wer():
    audio_path = os.path.join("tests", "audio", "sample.mp3")
    with open(audio_path, "rb") as f:
        audio_content = f.read()
    
    files = {
        'audio': ('sample.mp3', audio_content, 'audio/mpeg')
    }
    
    expected_text = "Help me, can't find my parents. They told me to wait for them, but I saw this pretty butterfly and followed it. Now I am lost."
    
    response = client.post("/stt/transcribe", files=files)
    assert response.status_code == 200
    
    # Calculate WER using jiwer
    error_rate = wer(expected_text, response.json()["transcript"])
    accuracy = (1.0 - error_rate) * 100
    
    print(f"\nReference: {expected_text}")
    print(f"Hypothesis: {response.json()['transcript']}")
    print(f"Word Error Rate: {error_rate:.2%}")
    print(f"Accuracy: {accuracy:.1f}%\n")
    
    assert error_rate <= 0.1  # 90% accuracy threshold