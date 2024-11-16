import os
from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
from routers import stt, database
from dotenv import load_dotenv
from utils.logger import logger

## Services
from services.pysqlite_service import get_sqlite_service
from services.vad_service import get_vad_service
from services.transcription_service import TranscriptionService


## Setup OS/DIR Path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## Load environment variables
load_dotenv(override=True)

# Initialize FastAPI
app = FastAPI()


async def startup():
    """
    Initialize services on application startup
    """
    
    try:
        # Initialize SQLite service. It will create the connection internally
        get_sqlite_service("transcriptions.db")
        
        # Initialize VAD service
        get_vad_service()

        # Initialize transcription service
        service = TranscriptionService(api_key=os.getenv("HF_TOKEN", ""))
        warm_up_success = await service.warm_up()
        if not warm_up_success:
            logger.warning("Model warm-up was not successful, but application will continue")
    except Exception as e:
        logger.warning(f"Error during initialization: {str(e)}. Application will start, but performance may be affected")
    
    logger.debug("Application startup completed")


async def shutdown():
    """
    Cleanup on application shutdown
    """
    
    logger.info("Application shutdown initiated")
    try:
        # Cleanup VAD service
        vad_service = get_vad_service()
        vad_service.cleanup()
        logger.info("VAD service cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up VAD service: {str(e)}")

# Add event handlers
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/health")
async def health_check():
    try:
        gmt_plus_8 = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))    
        return {
            "status": "ok",
            "timestamp": gmt_plus_8
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise
    
    
# Since we have only a few routers, add it directly here.
app.include_router(stt.router)
app.include_router(database.router)