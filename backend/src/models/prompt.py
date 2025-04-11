'''
Prompt models
'''
from sqlalchemy import Column, Integer, String, Text, DateTime
import sqlalchemy.sql.functions
from src.db.base import Base

class Prompt(Base):
    """
    Prompt Models
    """
    __tablename__ = "prompts"  # 明确指定表名
    __table_args__ = {"schema": "prompt"}  # 指定schema为prompt
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=sqlalchemy.sql.functions.now())
