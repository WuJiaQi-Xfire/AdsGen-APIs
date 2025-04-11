"""
Authentication related API endpoints
Provides user registration, login, and logout functionality
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_db
from src.core.security import create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.crud.user import user as user_crud
from src.schemas.user import User as UserSchema, UserCreate
from src.schemas.auth import Token, LoginResponse, LogoutResponse

# Create router
router = APIRouter()

# Add route description
router.description = "Authentication API, providing user registration, login, and logout functionality"

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=UserSchema, summary="User Registration")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    """
    User Registration API
    
    - **email**: User email address
    - **username**: Username for login
    - **password**: User password, will be hashed for storage
    - **full_name**: User's full name (optional)
    - **is_active**: Whether the user is active, default is True (optional)
    - **is_superuser**: Whether the user is a superuser, default is False (optional)
    
    Returns the created user information (excluding password)
    """
    try:
        # Check if email already exists
        user = await user_crud.get_by_attribute(db, attribute="email", value=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Check if username already exists
        user = await user_crud.get_by_attribute(db, attribute="username", value=user_in.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        
        # Create new user
        user = await user_crud.create(db, obj_in=user_in)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        ) from e

@router.post("/login", response_model=LoginResponse, summary="User Login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    User Login API
    
    - **username**: Username or email
    - **password**: User password
    
    Returns access token and token type
    """
    try:
        # Try to authenticate with email
        user = await user_crud.authenticate(db, email=form_data.username, password=form_data.password)
        
        # If email authentication fails, try with username
        if not user:
            # First get user by username
            user_by_username = await user_crud.get_by_attribute(db, attribute="username", value=form_data.username)
            if user_by_username:
                # Verify password
                user = await user_crud.authenticate(db, email=user_by_username.email, password=form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user_crud.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user",
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.user_id, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        ) from e

@router.post("/logout", response_model=LogoutResponse, summary="User Logout")
async def logout() -> LogoutResponse:
    """
    User Logout API
    
    Since JWT tokens are stateless, no server-side action is required.
    The client should delete the locally stored token.
    
    Returns a successful logout message
    """
    return {"detail": "Successfully logged out"}

@router.get("/me", response_model=UserSchema, summary="Get Current User")
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    """
    Get Current User API
    
    Retrieves the current authenticated user's information based on the provided JWT token.
    
    Returns the user information (excluding password)
    """
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_crud.get_by_attribute(db, attribute="user_id", value=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    return user
