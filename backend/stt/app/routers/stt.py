"""
Speech-to-Text transcription endpoint.

Pipeline:
1. Audio Validation - Verify file format and extract metadata
2. Preprocessing - Convert to 16kHz mono WAV
3. VAD - Remove silences using Silero model
4. Transcription - Process using HuggingFace API

Requires HF_TOKEN environment variable for HuggingFace authentication.
"""

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.audio_processor_service import AudioReader, AudioService
from services.pysqlite_service import get_sqlite_service
from services.vad_service import get_vad_service
from services.transcription_service import TranscriptionService
from utils.logger import logger


router = APIRouter(
    prefix="/stt",
    tags=["Speech to Text Transcription"],
    responses={
        404: {"description": "Not Found"}
    }
)


@router.post("/transcribe")
async def transcribe_file(audio: UploadFile = File(..., description="The audio file to transcribe")):
    if not audio.content_type.startswith('audio/'):
        raise HTTPException(
            status_code=400, 
            detail="File must be an audio file"
        )
    
    try:
        logger.debug("Starting transcription request.")
        
        ## Step 1: Retrieve audio metadata (e.g. audio format, sample rate)
        audio_reader = AudioReader(audio)
        audio_info = audio_reader.get_audio_info()
        logger.info(f"Audio detected and processing: {audio_info}")
        
        ## Step 2: Preprocess audio using output obtain from step 1 (e.g. Convert to .wav, convert to single channel, resample)
        audio_service = AudioService()
        audio_content_raw, audio_content_bytes = audio_reader.get_audio_content() # Keep audio_content_raw as a memory object of the original audio for any downstream operation
        processed_audio = await audio_service.preprocess_audio(audio_content=audio_content_bytes, audio_format=audio_info["audio_format"])
        
        ## Step 3: Apply VAD to remove silences from the preprocessed audio(step 2)
        vad_service = get_vad_service()
        vad_processed_audio = await vad_service.remove_silence(processed_audio)
        
        ## Step 4: Send final processed audio to transcription service (HuggingFace Inference API)
        transcription_service = TranscriptionService(api_key=os.getenv("HF_TOKEN"))
        result = await transcription_service.transcribe(vad_processed_audio)
        
        ## Step 5: Store transcription result in SQLite
        sqlite_service = get_sqlite_service()
        record_id = await sqlite_service.insert_transcription(
            file_name=audio_info["file_name"],
            audio_format=audio_info["audio_format"],
            channel=audio_info["channel"],
            sample_rate=audio_info["sample_rate"],
            duration=audio_info["duration"],
            transcription=result["text"]
        )
        
        if record_id is None:
            logger.error("Failed to store transcription in database")
            raise HTTPException(
                status_code=500,
                detail="Failed to store transcription result"
            )
            
        logger.info("Successfully inserted record into database")
            
        return {
            "metadata": audio_info,
            "transcript": result["text"],       
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in transcribing file: {str(e)}")