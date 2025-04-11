'''
Authentication schemas
'''
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class Token(BaseModel):
    """
    Token schema for authentication response
    """
    access_token: str
    token_type: str
    user_id: str
    username: str
    email: EmailStr
    is_superuser: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "johndoe",
                    "email": "user@example.com",
                    "is_superuser": False
                }
            ]
        }
    )

class TokenPayload(BaseModel):
    """
    Token payload schema for JWT token
    """
    sub: Optional[str] = None
    exp: Optional[int] = None

class LoginRequest(BaseModel):
    """
    Login request schema
    
    MANDATORY:
    - username: Username or email for login
    - password: User password
    """
    username: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "password": "strongpassword123"
                }
            ]
        }
    )

class LoginResponse(Token):
    """
    Login response schema
    """
    pass

class LogoutResponse(BaseModel):
    """
    Logout response schema
    """
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "detail": "Successfully logged out"
                }
            ]
        }
    )
