'''
Template models
'''
from sqlalchemy import Column, Integer, String, Text, DateTime
import sqlalchemy.sql.functions
from src.db.base import Base

class Template(Base):
    """
    Template Models
    """
    __tablename__ = "template" 
    __table_args__ = {"schema": "template"} 
    
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=sqlalchemy.sql.functions.now())