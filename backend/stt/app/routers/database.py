from fastapi import APIRouter, HTTPException, Query
from services.pysqlite_service import get_sqlite_service
from utils.logger import logger


router = APIRouter(
    prefix="/data",
    tags=["Database"],
    responses={
        404: {"description": "Not Found"}
    }
)


@router.get("/transcriptions")
async def get_all_transcriptions():
    try:
        sqlite_service = get_sqlite_service()
        transcriptions = await sqlite_service.get_all_transcriptions()
        
        return {
            "record": len(transcriptions),
            "data": transcriptions
        }
        
    except Exception as e:
        logger.error(f"Error retrieving transcriptions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve transcriptions from database"
        )


@router.get("/search")  # Changed to GET since we're retrieving data
async def search_transcriptions(
    keyword: str = Query(None, description="Search by file name or transcription content")
):
    try:
        if not keyword or not keyword.strip():
            raise HTTPException(
                status_code=400,
                detail="Search by file name or transcription content"
            )
            
        sqlite_service = get_sqlite_service()
        transcriptions = await sqlite_service.search_transcriptions(keyword.strip())
        
        return {
            "record": len(transcriptions),
            "data": transcriptions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching transcriptions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to search transcriptions"
        )
        
        
@router.delete("/delete_record")
async def delete_transcription(record_id: int):
    try:
        sqlite_service = get_sqlite_service()
        ## First check if record exists
        record = await sqlite_service.get_all_transcriptions()
        
        if not record:
            raise HTTPException(
                status_code=404,
                detail=f"Transcription with id {record_id} not found"
            )
        
        ## Delete the record
        success = await sqlite_service.delete_transcription(record_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete transcription"
            )
            
        return {
            "status": "success",
            "message": f"Record ID {record_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting transcription {record_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete transcription"
        )