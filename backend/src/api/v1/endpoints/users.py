'''
Endpoints for user rout
Inherent from CRUD router
'''
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import user as user_crud
from src.schemas.user import User as UserSchema, UserCreate, UserUpdate
from src.api.deps import CRUDRouter, get_db

# 使用CRUDRouter创建基本的CRUD路由
user_router = CRUDRouter[UserSchema, UserCreate, UserUpdate](user_crud)
router = user_router.router

# Add route description
router.description = "User Management API, " \
                     "providing functions for creating, querying, updating, and deleting users"
# Redefine routes to apply schema examples
@router.post("/", response_model=UserSchema, summary="Create New User")
async def create_user(item_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a New user
    
    - **email**: User email address
    - **username**: Username for login
    - **password**: User password, will be hashed for storage
    - **full_name**: User's full name (optional)
    - **is_active**: Whether the user is active, default is True (optional)
    - **is_superuser**: Whether the user is a superuser, default is False (optional)
    """
    try:
        return await user_router.create_item(item_in, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建用户失败: {str(e)}"
        ) from e

@router.get("/{item_id}", response_model=UserSchema, summary="Read a Single User")
async def read_user(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get user by ID
    
    - **item_id**: The ID of the user to retrieve
    
    Returns the user information if found, otherwise returns a 404 error.
    """
    try:
        return await user_router.read_item(item_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"查找用户失败: {str(e)}"
        ) from e

@router.put("/{item_id}", response_model=UserSchema, summary="Update User Information")
async def update_user(item_id: int, item_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update user information
    
    All fields are optional:
    - **email**: User email address
    - **username**: Username for login
    - **password**: User password, will be hashed for storage
    - **full_name**: User's full name
    - **is_active**: Whether the user is active
    - **is_superuser**: Whether the user is a superuser
    """
    return await user_router.update_item(item_id, item_in, db)

@router.delete("/{item_id}", response_model=UserSchema, summary="Delete User")
async def delete_user(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete user by ID
    
    - **item_id**: The ID of the user to delete
    
    Returns the deleted user information if found, otherwise returns a 404 error.
    """
    try:
        return await user_router.delete_item(item_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除用户失败: {str(e)}"
        ) from e

@router.get("/", response_model=List[UserSchema], summary="Read User List")
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Get list of users
    
    - **skip**: Number of users to skip (pagination)
    - **limit**: Maximum number of users to return (pagination)
    
    Returns a list of users, paginated according to skip and limit parameters.
    """
    try:
        # 获取 ORM 对象列表
        users = await user_router.read_items(skip=skip, limit=limit, db=db)
        users = [UserSchema.model_validate(user) for user in users]
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户列表失败: {str(e)+str(users)}"
        ) from e
