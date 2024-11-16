"""
This module provides services for audio processing in the transcription pipeline.

Key Responsibilities:
1. AudioReader
  - Extracts audio metadata
  - Retrieves sample rate and duration
  - Handles audio content loading

2. AudioService
  - Handles audio format conversion
  - Performs audio resampling to match model requirements
  - Standardizes audio processing

Dependencies:
- pydub: Audio processing library for format conversion and manipulation
"""

from io import BytesIO
from fastapi import File, UploadFile, HTTPException
from pydub.utils import mediainfo_json
from pydub import AudioSegment
from utils.logger import logger


class AudioReader:
    def __init__(self, audio_file: UploadFile = File(...)):
        try:
            self.file_name = audio_file.filename.split('/')[-1]
            self.file_content = audio_file.file.read() 
            self.file_bytes = BytesIO(self.file_content)
            __info = mediainfo_json(BytesIO(self.file_content))
            
            # Retrieve audio info from original audio data
            self.audio_format = str(__info['format']['format_name']).lower()
            self.channel = int(__info['streams'][0]['channels'])
            self.sample_rate = int(__info['streams'][0]['sample_rate'])
            self.duration = float(__info['streams'][0]['duration'])
            
        except Exception as e:
            error_message = f"Error while reading audio file: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=400, details=error_message)
        
        
    def __del__(self):
        ## Ensure that BytesIO is closed to prevent memory leak
        if hasattr(self, "file_bytes"):
            self.file_bytes.close()
        
        
    def get_audio_info(self):
        ## Return audio metadata as dictionary
        return {
            "file_name": self.file_name,
            "audio_format": self.audio_format,
            "channel": self.channel,
            "sample_rate": self.sample_rate,
            "duration": self.duration
        }
        
    def get_audio_content(self):
        ## Return both the file content and the BytesIO object
        return self.file_content, self.file_bytes
        
        
class AudioService:
    def __init__(self):
        self.target_sample_rate = 16000
        
        
    async def convert_to_wav(self, audio_content: BytesIO, audio_format: str):
        """
        Convert audio to WAV format if not already WAV. Lossless file format preserve more audio details which is needed for an accurate transcription.
        """
        
        audio_content.seek(0)  # Reset BytesIO position
        
        try:
            # Check if input is WAV format
            if audio_format == 'wav':
                logger.debug("Input is already in WAV format")
                audio = AudioSegment.from_wav(audio_content)
            else:
                # Convert non-WAV format to WAV
                logger.debug(f"Converting {audio_format} to WAV format")
                audio = AudioSegment.from_file(audio_content, format=audio_format)
                logger.info("Audio file converted to WAV format")
                
            return audio
            
        except Exception as e:
            error_message = f"Failed to process audio: {str(e)}"
            logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
            
            
    def convert_to_mono(self, audio: AudioSegment):
        """
        Convert audio to mono if it has multiple channels. Since Whisper is trained on mono audio, it reduces overall transcription error by transcribing a mono format audio.
        """
        
        if audio is None:
            error_message = "Audio input is None. Please ensure audio file was properly loaded."
            logger.error(error_message)
            raise HTTPException(status_code=400, detail=error_message)
            
        try:
            channels = audio.channels
            
            if channels > 1:
                logger.info(f"Converting {channels} channels to mono")
                audio = audio.set_channels(1)
                logger.debug("Successfully converted to mono")
            else:
                logger.debug(f"Audio already in mono ({channels} channel)")
                
            return audio
            
        except AttributeError as e:
            error_message = f"Invalid audio format - missing channels attribute: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=400, detail=error_message)
            
        except Exception as e:
            error_message = f"Error processing audio: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=400, detail=error_message)
    
    
    def resample_audio(self, audio: AudioSegment):
        """
        Resample audio to target sample rate if needed
        """
        try:
            if audio is None:
                raise ValueError("Audio input is None")
                
            current_rate = audio.frame_rate
            
            if current_rate != self.target_sample_rate:
                logger.info(f"Resampling audio from {current_rate}Hz to {self.target_sample_rate}Hz")
                try:
                    audio = audio.set_frame_rate(self.target_sample_rate)
                    logger.debug(f"Audio successfully resampled to {self.target_sample_rate}Hz")
                except Exception as e:
                    raise ValueError(f"Failed to resample audio: {str(e)}")
            else:
                logger.debug(f"Audio already at target sample rate of {self.target_sample_rate}Hz")
                
            return audio
            
        except Exception as e:
            error_message = f"Error in audio resampling: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=400, detail=error_message)

        
    async def preprocess_audio(self, audio_format, audio_content: BytesIO):
        try:
            ## Step 1 Convert to WAV format
            audio = await self.convert_to_wav(audio_content=audio_content, audio_format=audio_format)

            ## Step 2 Convert to mono channel
            audio = self.convert_to_mono(audio)
            
            ## Step 3 Resampling
            audio = self.resample_audio(audio)
            
            # Create preprocessed WAV output
            final_wav_buffer = BytesIO()
            audio.export(final_wav_buffer, format="wav")
            final_wav_buffer.seek(0)
            
            return final_wav_buffer
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error in converting and resampling audio: {str(e)}")