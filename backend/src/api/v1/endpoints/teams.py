'''
Endpoints for team routes
Inherent from CRUD router
'''
from typing import List, Optional
from fastapi import Depends, HTTPException, Path, Body, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.team import team as team_crud, team_member as team_member_crud
from src.schemas.team import Team as TeamSchema, TeamCreate, TeamUpdate
from src.schemas.team import TeamMember as TeamMemberSchema, TeamMemberCreate, TeamMemberUpdate
from src.api.deps import CRUDRouter, get_db
from src.models.user import User
from src.api.v1.endpoints.auth import get_current_user
from src.utils.permission import check_team_permission

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Use CRUDRouter to create basic CRUD routes for Team
team_router = CRUDRouter[TeamSchema, TeamCreate, TeamUpdate](team_crud)
router = team_router.router

# Add route description
router.description = "Team Management API, " \
                     "providing functions for creating, querying, updating, and deleting teams, " \
                     "as well as managing team members"

# Redefine routes to apply schema examples and add permission checks
@router.post("/", response_model=TeamSchema, summary="Create New Team")
async def create_team(
    item_in: TeamCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new team
    
    - **name**: Team name, must be unique
    - **description**: Team description (optional)
    
    The creator of the team will automatically be added as an admin.
    """
    try:
        # Check if can get current user
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get current user"
            )
        
        # Check if team with the same name already exists
        existing_team = await team_crud.get_by_name(db, name=item_in.name)
        if existing_team:
            raise HTTPException(
                status_code=400,
                detail=f"Team with name '{item_in.name}' already exists"
            )

        user_id = current_user.id
        # Create the team and add the creator as an admin in a single transaction
        team = await team_crud.create_team_with_admin(db, obj_in=item_in, user_id=user_id)
        return team
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create team: {str(e)}"
        ) from e

@router.get("/{item_id}", response_model=TeamSchema, summary="Read a Single Team")
async def read_team(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get team by ID
    
    - **item_id**: The ID of the team to retrieve
    
    Returns the team information if found, otherwise returns a 404 error.
    """
    try:
        return await team_router.read_item(item_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find team: {str(e)}"
        ) from e

@router.put("/{item_id}", response_model=TeamSchema, summary="Update Team Information")
async def update_team(
    item_id: int, 
    item_in: TeamUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update team information
    
    All fields are optional:
    - **name**: Team name
    - **description**: Team description
    
    Only team admins can update team information.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=item_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Check if user has permission (is superuser or team admin)
        has_permission = await check_team_permission(db, team_id=item_id, user_id=current_user.id, current_user=current_user)
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="Only team admins or superusers can update team information"
            )
        
        # Update the team
        return await team_router.update_item(item_id, item_in, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update team: {str(e)}"
        ) from e

@router.delete("/{item_id}", response_model=TeamSchema, summary="Delete Team")
async def delete_team(
    item_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete team by ID
    
    - **item_id**: The ID of the team to delete
    
    Only team admins can delete a team.
    Returns the deleted team information if found, otherwise returns a 404 error.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=item_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Check if user has permission (is superuser or team admin)
        has_permission = await check_team_permission(db, team_id=item_id, user_id=current_user.id, current_user=current_user)
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="Only team admins or superusers can delete a team"
            )
        
        # Delete the team
        return await team_router.delete_item(item_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete team: {str(e)}"
        ) from e

@router.get("/", response_model=List[TeamSchema], summary="Read Team List")
async def read_teams(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Get list of teams
    
    - **skip**: Number of teams to skip (pagination)
    - **limit**: Maximum number of teams to return (pagination)
    
    Returns a list of teams, paginated according to skip and limit parameters.
    """
    try:
        teams = await team_router.read_items(skip=skip, limit=limit, db=db)
        return teams
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get team list: {str(e)}"
        ) from e

# Team Member routes
@router.post("/{team_id}/members", response_model=TeamMemberSchema, summary="Add Team Member")
async def add_team_member(
    team_id: int = Path(..., description="The ID of the team"),
    member_in: TeamMemberCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a member to a team
    
    - **team_id**: The ID of the team
    - **user_id**: The ID of the user to add
    - **role**: The role of the user in the team (default: member)
    
    Only team admins can add members to a team.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Check if user has permission (is superuser or team admin)
        has_permission = await check_team_permission(db, team_id=team_id, user_id=current_user.id, current_user=current_user)
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="Only team admins or superusers can add members to a team"
            )
        
        # Check if user is already a member of the team
        existing_member = await team_member_crud.get_by_team_and_user(
            db, team_id=team_id, user_id=member_in.user_id
        )
        if existing_member:
            raise HTTPException(
                status_code=400,
                detail="User is already a member of this team"
            )
        
        # Create team member
        member_in.team_id = team_id  # Ensure team_id is set correctly
        team_member = await team_member_crud.create(db, obj_in=member_in)
        return team_member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add team member: {str(e)}"
        ) from e

@router.get("/{team_id}/members", response_model=List[TeamMemberSchema], summary="Get Team Members")
async def get_team_members(
    team_id: int = Path(..., description="The ID of the team"),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all members of a team
    
    - **team_id**: The ID of the team
    - **skip**: Number of members to skip (pagination)
    - **limit**: Maximum number of members to return (pagination)
    
    Returns a list of team members, paginated according to skip and limit parameters.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Get team members
        team_members = await team_member_crud.get_team_members(
            db, team_id=team_id, skip=skip, limit=limit
        )
        return team_members
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get team members: {str(e)}"
        ) from e

@router.put("/{team_id}/members/{user_id}", response_model=TeamMemberSchema, summary="Update Team Member")
async def update_team_member(
    team_id: int = Path(..., description="The ID of the team"),
    user_id: int = Path(..., description="The ID of the user"),
    member_in: TeamMemberUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a team member's role
    
    - **team_id**: The ID of the team
    - **user_id**: The ID of the user
    - **role**: The new role of the user in the team
    
    Only team admins can update team member roles.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Check if user has permission (is superuser or team admin)
        has_permission = await check_team_permission(db, team_id=team_id, user_id=current_user.id, current_user=current_user)
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="Only team admins or superusers can update team member roles"
            )
        
        # Check if user is a member of the team
        team_member = await team_member_crud.get_by_team_and_user(
            db, team_id=team_id, user_id=user_id
        )
        if not team_member:
            raise HTTPException(
                status_code=404,
                detail="User is not a member of this team"
            )
        
        # Update team member
        updated_member = await team_member_crud.update(db, db_obj=team_member, obj_in=member_in)
        return updated_member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update team member: {str(e)}"
        ) from e

@router.delete("/{team_id}/members/{user_id}", response_model=TeamMemberSchema, summary="Remove Team Member")
async def remove_team_member(
    team_id: int = Path(..., description="The ID of the team"),
    user_id: int = Path(..., description="The ID of the user"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a member from a team
    
    - **team_id**: The ID of the team
    - **user_id**: The ID of the user to remove
    
    Only team admins can remove members from a team.
    """
    try:
        # Check if team exists
        team = await team_crud.get(db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        
        # Check if user has permission (is superuser or team admin)
        has_permission = await check_team_permission(db, team_id=team_id, user_id=current_user.id, current_user=current_user)
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail="Only team admins or superusers can remove members from a team"
            )
        
        # Check if user is a member of the team
        team_member = await team_member_crud.get_by_team_and_user(
            db, team_id=team_id, user_id=user_id
        )
        if not team_member:
            raise HTTPException(
                status_code=404,
                detail="User is not a member of this team"
            )
        
        # Remove team member
        removed_member = await team_member_crud.remove(db, id=team_member.id)
        return removed_member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to remove team member: {str(e)}"
        ) from e
