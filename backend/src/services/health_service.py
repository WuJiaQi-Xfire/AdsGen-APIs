"""Module for health check services"""

import os
import asyncio
import logging
from typing import Dict, Any, List
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.db.session import engine
from src.services.comfy_service import COMFY_URL, check_comfy_available
from src.services.gpt_service import GPTService

logger = logging.getLogger(__name__)

class HealthService:
    """Service for checking health of various components"""
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connection"""
        try:
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                return {
                    "status": "healthy" if result else "unhealthy",
                    "message": "Database connection successful" if result else "Database connection failed"
                }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}"
            }
    
    async def check_comfyui(self) -> Dict[str, Any]:
        """Check ComfyUI connection"""
        try:
            if not COMFY_URL:
                return {
                    "status": "unhealthy",
                    "message": "ComfyUI URL not configured"
                }
            
            # First check if ComfyUI is available based on our initialization flag
            if check_comfy_available():
                return {
                    "status": "healthy",
                    "message": "ComfyUI connection successful"
                }
                
            # If not available based on initialization, try to connect directly
            async with httpx.AsyncClient() as client:
                # Try to connect to ComfyUI API with a shorter timeout
                response = await client.get(f"{COMFY_URL}/system_stats", timeout=2.0)
                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "message": "ComfyUI connection successful"
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "message": f"ComfyUI returned status code {response.status_code}"
                    }
        except Exception as e:
            logger.error(f"ComfyUI health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"ComfyUI connection failed: {str(e)}"
            }
    
    async def check_gpt(self) -> Dict[str, Any]:
        """Check GPT API connection"""
        try:
            gpt_service = GPTService()
            
            # Check if API key and endpoint are configured
            if not gpt_service.api_key or not gpt_service.api_endpoint:
                return {
                    "status": "unhealthy",
                    "message": "GPT API not configured properly"
                }
            
            # Use a simpler test for GPT API to reduce response time
            # Try a very simple API call with minimal tokens
            test_data = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Health check"
                    },
                    {
                        "role": "user",
                        "content": "OK?"
                    }
                ],
                "max_tokens": 1
            }
            
            # Set a timeout for the API call
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(gpt_service.make_api_call, test_data),
                    timeout=2.0
                )
                
                if response and isinstance(response, str):
                    return {
                        "status": "healthy",
                        "message": "GPT API connection successful"
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "message": "GPT API returned unexpected response"
                    }
            except asyncio.TimeoutError:
                return {
                    "status": "unhealthy",
                    "message": "GPT API request timed out after 2 seconds"
                }
        except Exception as e:
            logger.error(f"GPT API health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"GPT API connection failed: {str(e)}"
            }
    
    async def check_frontend_backend(self) -> Dict[str, Any]:
        """Check frontend-backend communication"""
        # This is always healthy if the API is reachable
        return {
            "status": "healthy",
            "message": "Frontend-backend communication successful"
        }
    
    async def check_all_services(self) -> Dict[str, Any]:
        """Check all services and return their status"""
        results = await asyncio.gather(
            self.check_database(),
            self.check_comfyui(),
            self.check_gpt(),
            self.check_frontend_backend()
        )
        
        return {
            "database": results[0],
            "comfyui": results[1],
            "gpt": results[2],
            "frontend_backend": results[3],
            "all_healthy": all(result["status"] == "healthy" for result in results)
        }

health_service = HealthService()
