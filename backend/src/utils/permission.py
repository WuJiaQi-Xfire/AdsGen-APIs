"""
Permission utility functions for team management
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.crud.team import team_member as team_member_crud

async def check_team_permission(
    db: AsyncSession, 
    team_id: int, 
    user_id: int, 
    current_user: User
) -> bool:
    """
    Check if a user has permission to perform operations on a team
    
    Args:
        db: Database session
        team_id: Team ID
        user_id: User ID
        current_user: Current authenticated user
        
    Returns:
        True if the user has permission (is a superuser or team admin), False otherwise
    """
    # Superusers can perform any operation
    if current_user.is_superuser:
        return True
    
    # Check if user is a team admin
    is_admin = await team_member_crud.is_team_admin(db, team_id=team_id, user_id=user_id)
    return is_admin
