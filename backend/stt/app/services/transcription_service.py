"""
This module provides TranscriptionService class for managing HuggingFace's Whisper model transcription.

Key Responsibilities:
1. Model Warm-up
   - Initializes model at application startup via dummy audio request
   - Ensures model is ready for first user request
   - Configurable retry mechanism via environment variables:
     - HF_MAX_RETRIES: Maximum number of retry attempts
     - HF_RETRY_DELAY: Initial delay between retries (seconds)

2. Transcription Handling
   - Manages transcription requests to HuggingFace inference API
   - Performs model readiness check
   - Automatically initiates warm-up if model is not loaded
"""


import os
import time
import wave
import requests
from io import BytesIO
from fastapi import HTTPException
from utils.logger import logger

class TranscriptionService:
    def __init__(self, api_key: str = ""):
        """
        Initialize the transcription service.
        """
        self.model = os.getenv("WHISPER_MODEL", "openai/whisper-tiny")
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.max_retries = int(os.getenv("HF_MAX_RETRIES", "5"))
        self.retry_delay = int(os.getenv("HF_RETRY_DELAY", "2"))
        logger.info(f"Initialized TranscriptionService with model: {self.model}")

    def _create_dummy_wav(self) -> BytesIO:
        """
        Create a minimal WAV file for warm-up. In-memory buffer that acts like a file. Clean up by Python automatically once it is not being reference.
        """
        
        buffer = BytesIO()
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1)  # mono
            wav.setsampwidth(2)  # 2 bytes per sample
            wav.setframerate(16000)  # 16kHz
            wav.writeframes(b'\x00' * 16000)  # 1 second of silence
        buffer.seek(0)
        return buffer

    async def warm_up(self) -> bool:
        """
        Warm up the model with a minimal WAV file.
        """
        
        logger.info(f"Warming up model: {self.model}")
        
        # Create a dummy WAV file
        audio_data = self._create_dummy_wav()
        
        for attempt in range(self.max_retries):
            try:
                # Reset buffer position
                audio_data.seek(0)
                
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=audio_data.read()
                )
                
                # Log response for debugging
                logger.debug(f"Warm-up response status: {response.status_code}")
                if response.content:
                    logger.debug(f"Warm-up response content: {response.content[:200]}")
                
                if response.status_code == 200:
                    logger.info(f"Model {self.model} successfully loaded")
                    return True
                    
                elif response.status_code == 503:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.info(f"Model still loading. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    logger.error(f"Unexpected status code during warm-up: {response.status_code}")
                    if response.content:
                        logger.error(f"Error response: {response.content}")
                    return False
                    
            except Exception as e:
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Warm-up attempt {attempt + 1} failed: {str(e)}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        logger.error(f"Failed to warm up model after {self.max_retries} attempts")
        return False


    async def transcribe(self, audio_data: BytesIO):
        """
        Transcribe audio using Hugging Face API.
        """
        
        try:
            # Reset buffer position
            audio_data.seek(0)
            
            # Send request to Hugging Face API
            logger.debug("Sending request to Hugging Face API")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=audio_data.read()
            )
            
            # If model is still loading, retry with backoff
            if response.status_code == 503:
                logger.debug("Model not ready. Starting warm-up sequence...")
                await self.warm_up()
                
                # Retry the transcription after warm-up
                audio_data.seek(0)
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=audio_data.read()
                )
            
            result = response.json()
            logger.debug("Successfully received transcription from API")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Transcription API request failed: {str(e)}"
            )
        except ValueError as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to parse transcription response"
            )