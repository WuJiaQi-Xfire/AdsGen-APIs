import pytest
from src.database.database import DatabaseManager
import os
import tempfile


@pytest.fixture
def db_manager():
    """Fixture to create a temporary database for testing"""
    # Use a temporary file for testing to avoid affecting the main database
    temp_db_path = os.path.join(tempfile.gettempdir(), 'test_prompts.db')
    
    try:
        # Create a new database manager with the temporary database
        db = DatabaseManager(db_path=temp_db_path)
        
        # Ensure the database is set up
        db.create_tables()
        
        yield db
    finally:
        # Clean up: remove the temporary database file after tests
        try:
            os.unlink(temp_db_path)
        except Exception:
            pass
