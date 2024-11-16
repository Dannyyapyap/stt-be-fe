"""
This module provides services for audio processing in the transcription pipeline.

Key Responsibilities:
1) Voice Activity Detection (VADService) for removing silences from audio

Implementation Details:
1) Singleton pattern for VADService ensures single model initialization
2) Model is loaded at startup and reused throughout application lifecycle
3) Processes audio in chunks of 512 samples (optimized for 16kHz)
4) Uses configurable threshold for silence detection (0.0 to 1.0)
   - Lower values (e.g., 0.3) = less aggressive, keeps more audio
   - Higher values (e.g., 0.7) = more aggressive silence removal

Audio Requirements:
- Input must be preprocessed to 16kHz sample rate
- Input must be single channel (mono)
- Audio format must be WAV

Dependencies:
1) silero-vad package
2) soundfile: For audio I/O operations

Usage:
    vad_service = get_vad_service()  # Get singleton instance
    processed_audio = await vad_service.remove_silence(
        audio_content,    # BytesIO object containing 16kHz mono WAV
        threshold=0.3     # Optional: adjust silence detection sensitivity
    )
"""

import os
from io import BytesIO
import numpy as np
import soundfile as sf
from silero_vad import load_silero_vad, get_speech_timestamps  
from utils.logger import logger


class VADService:
    _instance = None # Class variable to be shared across all instances, None initially until it is called for the first time
    
    def __init__(self):
        if not hasattr(self, 'model'):
            self.model = load_silero_vad()
            logger.info("Silero VAD model initialized successfully")
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None: # Check if instance exists
            cls._instance = cls() # If not, create an instance of VADService to be shared throughout the lifecycle. Equivalent to calling VADService __init__ method
        return cls._instance

    async def remove_silence(self, audio_content: BytesIO):
        """
        Remove silence from audio using VAD following Silero's documentation.
        Audio is expected to be 16kHz mono WAV.
        """
        
        try:
            logger.debug("Applying VAD to remove silence")
            
            # Load audio from BytesIO
            wav, sr = sf.read(audio_content)
            
            # Get speech timestamps using Silero's utility
            speech_timestamps = get_speech_timestamps(
                wav,
                self.model,
                threshold=float(os.getenv("VAD_THRESHOLD", 0.3)),
                return_seconds=False
            )
            
            # Initialize array for processed audio
            processed_segments = []
            
            # Extract speech segments
            for ts in speech_timestamps:
                processed_segments.append(wav[ts['start']:ts['end']])
            
            # Concatenate all segments
            processed_audio = np.concatenate(processed_segments)
            
            # Save processed audio
            output_buffer = BytesIO()
            sf.write(output_buffer, processed_audio, sr, format='WAV')
            output_buffer.seek(0)
            return output_buffer

        except Exception as e:
            logger.error(f"Error in silence removal: {str(e)}")
            raise

    def cleanup(self):
        """Clean up model resources"""
        if hasattr(self, 'model'):
            self.model = None
            logger.info("VAD model cleaned up")


def get_vad_service():
    """Get the singleton instance of VADService"""
    return VADService.get_instance()