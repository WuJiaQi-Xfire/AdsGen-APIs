from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from datetime import datetime

# Create router
router = APIRouter()

# Test Route - Return simple text message
@router.get("/hello")
async def hello_world() -> Dict[str, str]:
    """
    Return a simple hello message
    """
    return {"message": "Hello, world! This is a test route."}

# Test Route - Return current time
@router.get("/time")
async def current_time() -> Dict[str, str]:
    """
    Return the current server time
    """
    now = datetime.now()
    return {"current_time": now.strftime("%Y-%m-%d %H:%M:%S")}
