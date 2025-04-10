'''
User schemas
'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel,ConfigDict,EmailStr

# Shared properties
class UserBase(BaseModel):
    """
    User basic properties
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Properties required when creating a new user
class UserCreate(UserBase):
    """
    MANDATORY:
    - email: User email address
    - username: Username for login
    - password: User password, will be hashed for storage

    OPTIONAL:
    - full_name: User full name
    - is_active: User is active, default is True
    - is_superuser: Whether the user is a superuser, default is False
    """
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
                "examples": [
                    {
                        "email": "user@example.com",
                        "username": "johndoe",
                        "password": "strongpassword123",
                        "full_name": "John Doe",
                        "is_active": True,
                        "is_superuser": False
                    }
                ]
            }
    )

# Update user properties that can be updated
class UserUpdate(UserBase):
    """
    OPTIONAL:
    - email: User email address
    - username: Username for login
    - password: User password, will be hashed for storage
    - full_name: User full name
    - is_active: User is active
    - is_superuser: Whether the user is a superuser
    """
    password: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "user@example.com",
                    "username": "johndoe",
                    "password": "newstrongpassword123",
                    "full_name": "John Doe",
                    "is_active": True,
                    "is_superuser": False
                }
            ]
        }
    )


#  User properties stored in the database
class UserInDBBase(UserBase):
    """
    User basic properties stored in the database
    """
    id: Optional[int] = None
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Return user information to the API, excluding sensitive data such as password hashes
class User(UserInDBBase):
    """
    Return user information to the API, excluding sensitive data such as password hashes
    """
    model_config = ConfigDict(from_attributes=True)



# User information stored in the database, including password hashes
class UserInDB(UserInDBBase):
    """
    Complete user information stored in the database, including password hashes
    Note: This model is generally used internally and should not be exposed directly to the API
    """
    hashed_password: str
