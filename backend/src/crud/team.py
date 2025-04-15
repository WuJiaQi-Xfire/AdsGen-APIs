from typing import Any, Dict, Optional, Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.crud.base import CRUDBase
from src.models.team import Team as TeamModel, TeamMember as TeamMemberModel
from src.schemas.team import TeamCreate, TeamUpdate, TeamMemberCreate, TeamMemberUpdate

class CRUDTeam(CRUDBase[TeamModel, TeamCreate, TeamUpdate]):
    """
    CRUD operations for Team
    """
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[TeamModel]:
        """
        Get team by name
        
        Args:
            db: Database session
            name: Team name
            
        Returns:
            Team object if found, None otherwise
        """
        result = await db.execute(select(TeamModel).filter(TeamModel.name == name))
        return result.scalars().first()
    
    async def create_team_with_admin(
        self, db: AsyncSession, *, obj_in: TeamCreate, user_id: int
    ) -> TeamModel:
        """
        Create a new team and add the creator as an admin in a single transaction
        
        Args:
            db: Database session
            obj_in: Team creation data
            user_id: ID of the user to be added as admin
            
        Returns:
            Created team object
        """
        # Create team object from input data
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        
        # Flush to get the team ID without committing the transaction
        await db.flush()
        
        # Create team member object for the admin
        team_member_data = TeamMemberCreate(
            team_id=db_obj.id,
            user_id=user_id,
            role="admin"
        )
        team_member_obj_data = team_member_data.model_dump()
        team_member_db_obj = TeamMemberModel(**team_member_obj_data)
        db.add(team_member_db_obj)
        
        # Commit all changes in a single transaction
        await db.commit()
        await db.refresh(db_obj)
        
        return db_obj

class CRUDTeamMember(CRUDBase[TeamMemberModel, TeamMemberCreate, TeamMemberUpdate]):
    """
    CRUD operations for TeamMember
    """
    async def get_by_team_and_user(
        self, db: AsyncSession, *, team_id: int, user_id: int
    ) -> Optional[TeamMemberModel]:
        """
        Get team member by team_id and user_id
        
        Args:
            db: Database session
            team_id: Team ID
            user_id: User ID
            
        Returns:
            TeamMember object if found, None otherwise
        """
        result = await db.execute(
            select(TeamMemberModel).filter(
                and_(
                    TeamMemberModel.team_id == team_id,
                    TeamMemberModel.user_id == user_id
                )
            )
        )
        return result.scalars().first()
    
    async def get_team_members(
        self, db: AsyncSession, *, team_id: int, skip: int = 0, limit: int = 100
    ) -> List[TeamMemberModel]:
        """
        Get all members of a team
        
        Args:
            db: Database session
            team_id: Team ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of TeamMember objects
        """
        result = await db.execute(
            select(TeamMemberModel)
            .filter(TeamMemberModel.team_id == team_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_user_teams(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[TeamMemberModel]:
        """
        Get all teams a user is a member of
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of TeamMember objects
        """
        result = await db.execute(
            select(TeamMemberModel)
            .filter(TeamMemberModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def is_team_admin(
        self, db: AsyncSession, *, team_id: int, user_id: int
    ) -> bool:
        """
        Check if a user is an admin of a team
        
        Args:
            db: Database session
            team_id: Team ID
            user_id: User ID
            
        Returns:
            True if the user is an admin of the team, False otherwise
        """
        team_member = await self.get_by_team_and_user(db, team_id=team_id, user_id=user_id)
        if team_member and team_member.role == "admin":
            return True
        return False

# Create instances of the CRUD classes
team = CRUDTeam(TeamModel)
team_member = CRUDTeamMember(TeamMemberModel)
