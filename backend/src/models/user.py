'''
User models
'''
import uuid
from sqlalchemy import Boolean, Column, Integer, String, DateTime
import sqlalchemy.sql.functions
from src.db.base import Base

class User(Base):
    """
    User Models
    """
    __tablename__ = "users"  # 明确指定表名
    __table_args__ = {"schema": "user"}  # 指定schema为user
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False,
                    default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=sqlalchemy.sql.functions.now())
    updated_at = Column(DateTime(timezone=True), onupdate=sqlalchemy.sql.functions.now())
