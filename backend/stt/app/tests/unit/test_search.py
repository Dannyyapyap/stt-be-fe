"""
Unit test for the SQLite data pipeline. This test verifies:
1. Get all transcriptions record successfully (With mock data and empty list)
2. Search using keyword on mock data for two scenario, matching and non-matching search
"""

import pytest
from unittest.mock import MagicMock
from services.pysqlite_service import SQLiteService


mock_records = [
        {
            "record":1, 
            "data": [
                {
                    "id": 1, 
                    "file_name": "sample.mp3", 
                    "audio_format": "mp3", 
                    "channel": 1, 
                    "sample_rate": 48000, 
                    "transcription": "sample content that is being tested", 
                    "created_at": "2024-11-14 18:05:41"
                },
                {
                    "id": 1, 
                    "file_name": "sample2.mp3", 
                    "audio_format": "mp3", 
                    "channel": 1, 
                    "sample_rate": 41600, 
                    "transcription": "second content that is being tested", 
                    "created_at": "2024-12-12 15:12:42"
                }]
            }
        ]


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.cursor = MagicMock()
    return db

@pytest.fixture
def sqlite_service(mock_db):
    service = SQLiteService()
    service.db = mock_db
    return service


"""
Unit test for get_all_transcriptions(with records and no record)
"""
@pytest.mark.asyncio
async def test_get_all_transcriptions_success(sqlite_service, mock_db):
    
    mock_db.cursor.fetchall.return_value = mock_records
    
    result = await sqlite_service.get_all_transcriptions()
    
    mock_db.cursor.execute.assert_called_once_with(
        "SELECT * FROM transcription_result ORDER BY created_at DESC"
    )
    assert result == mock_records

@pytest.mark.asyncio
async def test_get_all_transcriptions_empty(sqlite_service, mock_db):
    mock_db.cursor.fetchall.return_value = []
    result = await sqlite_service.get_all_transcriptions()
    assert result == []


"""
Unit test for Search (with result, no result and no input)
"""
@pytest.mark.asyncio
async def test_search_transcriptions_success(sqlite_service, mock_db):
    mock_db.cursor.fetchall.return_value = mock_records
    
    result = await sqlite_service.search_transcriptions("sample")
    
    mock_db.cursor.execute.assert_called_once_with(
        """
                SELECT * FROM transcription_result 
                WHERE file_name LIKE ? 
                OR transcription LIKE ?
                ORDER BY created_at DESC
            """,
        ('%sample%', '%sample%')
    )
    assert result == mock_records

@pytest.mark.asyncio
async def test_search_transcriptions_no_results(sqlite_service, mock_db):
    mock_db.cursor.fetchall.return_value = []
    result = await sqlite_service.search_transcriptions("nonexistent_record")
    assert result == []