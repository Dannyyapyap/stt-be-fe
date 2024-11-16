"""
SQLite service for managing audio transcription records.

Key Responsibilities:
1) Database initialization and connection handling
2) CRUD operations for transcription data
3) Search functionality for stored records

Implementation Details:
1) Singleton pattern ensures a single database instance across the application
2) Manual database connection management within the service

Schema (transcription_result):
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- file_name: TEXT
- audio_format: TEXT
- channel: INTEGER
- sample_rate: INTEGER
- duration: REAL
- transcription: TEXT
- created_at: TEXT DEFAULT CURRENT_TIMESTAMP
"""

import sqlite3
from pathlib import Path
from pydantic import BaseModel
from utils.logger import logger

class Database(BaseModel):
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor
    
    class Config:
        arbitrary_types_allowed = True


def get_connection(db_path: str):
    """Helper function to create a database connection with row factory"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


class SQLiteService:
    _instance = None  # Class variable for singleton instance
    
    def __init__(self, db_path: str = "transcriptions.db"):
        root_dir = Path(__file__).parent.parent.parent
        self.db_path = root_dir / db_path
        self._initialized = False
        self.db = None


    @classmethod
    def get_instance(cls, db_path: str = "transcriptions.db"):
        if cls._instance is None:
            cls._instance = cls(db_path)
            cls._instance._initialize_db()  # Initialize the db connection once here
        return cls._instance


    def _initialize_db(self):
        """Initialize the SQLite database and create transcription_result table"""
        
        if self._initialized:
            return
        
        try:
            # Ensure the directory for the database file exists, creating it if necessary
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Create and store the Database connection in the service instance
            conn = get_connection(self.db_path)
            cursor = conn.cursor()
            self.db = Database(conn=conn, cursor=cursor) # Create a Database object to hold the connection and cursor, enabling access to the database for CRUD operations

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transcription_result (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    audio_format TEXT,
                    channel INTEGER,
                    sample_rate INTEGER,
                    duration REAL,
                    transcription TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info(f"SQLite database initialized at {self.db_path}")
            self._initialized = True

        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise


    async def insert_transcription(
        self,
        file_name: str,
        audio_format: str,
        channel: int,
        sample_rate: int,
        duration: float,
        transcription: str
    ):
        """Insert a transcription record with all metadata"""
        
        try:
            ## Using parameterized input ? to prevent SQL Injection
            self.db.cursor.execute(
                """INSERT INTO transcription_result 
                   (file_name, audio_format, channel, sample_rate, duration, transcription)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (file_name, audio_format, channel, sample_rate, duration, transcription)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Failed to insert transcription: {str(e)}")
            return None


    async def get_all_transcriptions(self):
        """Get all transcriptions ordered by creation date descending"""
        
        try:
            self.db.cursor.execute("SELECT * FROM transcription_result ORDER BY created_at DESC")
            records = self.db.cursor.fetchall()
            return [dict(record) for record in records] if records else []
                    
        except Exception as e:
            logger.error(f"Failed to get transcriptions: {str(e)}")
            return []


    async def search_transcriptions(self, search_term: str):
        """
        Search transcriptions by file name or transcription content
        Uses case-insensitive partial matching
        """
        
        try:
            self.db.cursor.execute("""
                SELECT * FROM transcription_result 
                WHERE file_name LIKE ? 
                OR transcription LIKE ?
                ORDER BY created_at DESC
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            records = self.db.cursor.fetchall()
            return [dict(record) for record in records] if records else []
                    
        except Exception as e:
            logger.error(f"Failed to search transcriptions: {str(e)}")
            return []


    async def delete_transcription(self, record_id: int) -> bool:
        """Delete a transcription by ID"""
        
        try:
            self.db.cursor.execute("DELETE FROM transcription_result WHERE id = ?", (record_id,))
            self.db.conn.commit()
            return self.db.cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Failed to delete transcription {record_id}: {str(e)}")
            return False

# Default db created will be transcriptions.db, so we'll include it as a fallback.
def get_sqlite_service(db_path: str = "transcriptions.db"):
    return SQLiteService.get_instance(db_path)
