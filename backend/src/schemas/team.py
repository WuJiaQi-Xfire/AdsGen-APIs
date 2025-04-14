'''
Team schemas
'''
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Shared properties for Team
class TeamBase(BaseModel):
    """
    Team basic properties
    """
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Properties required when creating a new team
class TeamCreate(TeamBase):
    """
    MANDATORY:
    - name: Team name, must be unique

    OPTIONAL:
    - description: Team description
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Development Team",
                    "description": "Team responsible for software development"
                }
            ]
        }
    )

# Properties that can be updated
class TeamUpdate(TeamBase):
    """
    OPTIONAL:
    - name: Team name
    - description: Team description
    """
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Development Team Updated",
                    "description": "Updated description for the development team"
                }
            ]
        }
    )

# Team properties stored in the database
class TeamInDBBase(TeamBase):
    """
    Team properties stored in the database
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Return team information to the API
class Team(TeamInDBBase):
    """
    Return team information to the API
    """
    model_config = ConfigDict(from_attributes=True)

# Shared properties for TeamMember
class TeamMemberBase(BaseModel):
    """
    Team Member basic properties
    """
    team_id: int
    user_id: int
    role: str = "member"  # Default role is member

    model_config = ConfigDict(from_attributes=True)

# Properties required when creating a new team member
class TeamMemberCreate(TeamMemberBase):
    """
    MANDATORY:
    - team_id: ID of the team
    - user_id: ID of the user

    OPTIONAL:
    - role: Role of the user in the team (default: member)
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "team_id": 1,
                    "user_id": 1,
                    "role": "admin"
                }
            ]
        }
    )

# Properties that can be updated
class TeamMemberUpdate(BaseModel):
    """
    OPTIONAL:
    - role: Role of the user in the team
    """
    role: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "role": "admin"
                }
            ]
        }
    )

# TeamMember properties stored in the database
class TeamMemberInDBBase(TeamMemberBase):
    """
    TeamMember properties stored in the database
    """
    id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Return team member information to the API
class TeamMember(TeamMemberInDBBase):
    """
    Return team member information to the API
    """
    model_config = ConfigDict(from_attributes=True)
