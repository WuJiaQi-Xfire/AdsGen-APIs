'''
Endpoints for prompt route
Inherent from CRUD router
'''
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.prompt import prompt as prompt_crud
from src.schemas.prompt import Prompt as PromptSchema, PromptCreate, PromptUpdate
from src.api.deps import CRUDRouter, get_db

# Use CRUDRouter to create basic CRUD routes
prompt_router = CRUDRouter[PromptSchema, PromptCreate, PromptUpdate](prompt_crud)
router = prompt_router.router

# Add route description
router.description = "Prompt Management API, " \
                     "providing functions for creating, querying, updating, and deleting prompts"

@router.post("/", response_model=PromptSchema, summary="Create New Prompt")
async def create_prompt(item_in: PromptCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new prompt
    
    - **prompt_name**: Prompt name
    - **content**: Prompt content
    """
    try:
        return await prompt_router.create_item(item_in, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create prompt: {str(e)}"
        ) from e

@router.get("/{item_id}", response_model=PromptSchema, summary="Read a Single Prompt")
async def read_prompt(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get prompt by ID
    
    - **item_id**: The ID of the prompt to retrieve
    
    Returns the prompt information if found, otherwise returns a 404 error.
    """
    try:
        return await prompt_router.read_item(item_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find prompt: {str(e)}"
        ) from e

@router.put("/{item_id}", response_model=PromptSchema, summary="Update Prompt Information")
async def update_prompt(item_id: int, item_in: PromptUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update prompt information
    
    All fields are optional:
    - **prompt_name**: Prompt name
    - **content**: Prompt content
    """
    try:
        return await prompt_router.update_item(item_id, item_in, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update prompt: {str(e)}"
        ) from e

@router.delete("/{item_id}", response_model=PromptSchema, summary="Delete Prompt")
async def delete_prompt(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete prompt by ID
    
    - **item_id**: The ID of the prompt to delete
    
    Returns the deleted prompt information if found, otherwise returns a 404 error.
    """
    try:
        return await prompt_router.delete_item(item_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete prompt: {str(e)}"
        ) from e

@router.get("/", response_model=List[PromptSchema], summary="Read Prompt List")
async def read_prompts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Get list of prompts
    
    - **skip**: Number of prompts to skip (pagination)
    - **limit**: Maximum number of prompts to return (pagination)
    
    Returns a list of prompts, paginated according to skip and limit parameters.
    """
    try:
        # Get list of ORM objects
        prompts = await prompt_router.read_items(skip=skip, limit=limit, db=db)
        prompts = [PromptSchema.model_validate(prompt) for prompt in prompts]
        return prompts
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get prompt list: {str(e)}"
        ) from e
