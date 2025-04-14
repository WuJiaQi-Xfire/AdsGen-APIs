'''
Team models
'''
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
import sqlalchemy.sql.functions
from src.db.base import Base

class Team(Base):
    """
    Team Models
    """
    __tablename__ = "team"  # Table name
    __table_args__ = {"schema": "team"}  # Specify schema as team
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=sqlalchemy.sql.functions.now())

class TeamMember(Base):
    """
    Team Member Models
    """
    __tablename__ = "team_members"  # Table name
    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_member"),
        {"schema": "team"}  # Specify schema as team
    )
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.team.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False, default="member")  # Options: admin, member
    joined_at = Column(DateTime(timezone=True), server_default=sqlalchemy.sql.functions.now())
