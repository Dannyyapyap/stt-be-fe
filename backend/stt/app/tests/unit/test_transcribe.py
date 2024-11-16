"""
Unit test for the STT transcription service pipeline. This test verifies:
1. AudioReader service to retrieve audio metadata
2. AudioService service to pre-process audio (Convert to WAV, convert to Mono channel, resample to 16kHz)
3. VADService service to remove silences from pre-processed audio chunks
4. TranscriptionService to transcribe audio by calling HuggingFace Inference API
5. SQLiteService to initialize DB and insert record
"""

import os
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch

client = TestClient(app)

def test_transcribe_expected_text():
    audio_path = os.path.join("tests", "audio", "sample.mp3")
    with open(audio_path, "rb") as f:
        audio_content = f.read()
    
    files = {
        'audio': ('sample.mp3', audio_content, 'audio/mpeg')
    }
    
    expected_text = " Help me, can't find my parents. They told me to wait for them, but I saw this pretty butterfly and followed it. Now I am lost."
    
    with patch('services.audio_processor_service.AudioReader') as MockAudioReader, \
         patch('services.audio_processor_service.AudioService') as MockAudioService, \
         patch('services.vad_service.get_vad_service') as mock_get_vad, \
         patch('services.transcription_service.TranscriptionService') as MockTransService, \
         patch('services.pysqlite_service.get_sqlite_service') as mock_get_sqlite:
        
        mock_reader = MockAudioReader.return_value
        mock_reader.get_audio_info.return_value = {
            "file_name": "sample.mp3",
            "audio_format": "mp3",
            "channel": 1,
            "sample_rate": 48000,
            "duration": 11.088
        }
        
        mock_reader.get_audio_content.return_value = (audio_content, audio_content)

        MockAudioService.return_value.preprocess_audio = AsyncMock(return_value=audio_content)
        mock_get_vad.return_value.remove_silence = AsyncMock(return_value=audio_content)
        MockTransService.return_value.transcribe = AsyncMock(return_value={"text": expected_text})
        mock_get_sqlite.return_value.insert_transcription = AsyncMock(return_value=1)

        response = client.post("/stt/transcribe", files=files)
        
        assert response.status_code == 200
        assert response.json()["transcript"] == expected_text