from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum
from typing import List

from src.db.session import get_db
from src.api.v1.endpoints.auth import get_current_user
from src.models.user import User

router = APIRouter()

class TableType(str, Enum):
    """Enum for database table types that can be cleared"""
    USERS = "users"
    TEAMS = "teams"
    PROMPTS = "prompts"
    ALL = "all"

@router.post("/clear-tables", summary="Clear Database Tables")
async def clear_tables(
    table_types: List[TableType],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Clear specified database tables. This operation is irreversible and will delete all data in the specified tables.
    
    - **table_types**: List of table types to clear (users, teams, prompts, or all)
    
    This endpoint requires superuser privileges.
    """
    # Check if user is superuser
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can perform this operation"
        )
    
    try:
        tables_cleared = []
        
        # Check if ALL is in the list
        if TableType.ALL in table_types:
            table_types = [TableType.USERS, TableType.TEAMS, TableType.PROMPTS]
        
        # Clear team tables
        if TableType.TEAMS in table_types:
            # First clear team_members due to foreign key constraints
            await db.execute(text("DELETE FROM team.team_members"))
            await db.execute(text("DELETE FROM team.team"))
            tables_cleared.append("team.team_members")
            tables_cleared.append("team.team")
        
        # Clear prompt tables
        if TableType.PROMPTS in table_types:
            await db.execute(text("DELETE FROM prompt.prompts"))
            tables_cleared.append("prompt.prompts")
        
        # Clear user tables (should be last due to foreign key references)
        if TableType.USERS in table_types:
            # Check if the current user is being deleted
            current_user_id = current_user.id
            # Keep the current superuser
            await db.execute(text(f"DELETE FROM \"user\".users WHERE id != {current_user_id}"))
            tables_cleared.append("user.users (except current superuser)")
        
        # Commit the transaction
        await db.commit()
        
        return {
            "status": "success",
            "message": "Tables cleared successfully",
            "tables_cleared": tables_cleared
        }
    
    except SQLAlchemyError as e:
        # Rollback in case of error
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        # Rollback in case of error
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing tables: {str(e)}"
        )

@router.get("/db", summary="Test Database Connection")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    """
    Test database connection and basic operations to verify the availability of the database system.
    
    Returns database connection information and version.
    """
    try:
        # 获取PostgreSQL版本
        version_result = await db.execute(text("SELECT version()"))
        version = version_result.scalar()
        
        # 获取当前数据库名称
        db_name_result = await db.execute(text("SELECT current_database()"))
        db_name = db_name_result.scalar()
        
        # 获取当前用户
        user_result = await db.execute(text("SELECT current_user"))
        user = user_result.scalar()
        
        # 获取所有表名
        tables_result = await db.execute(
            text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """)
        )
        tables_rows = tables_result.all()
        
        tables = [table[0] for table in tables_rows]
        
        return {
            "status": "success",
            "database": {
                "version": version,
                "name": db_name,
                "user": user,
                "tables": tables
            }
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"数据库连接错误: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"未知错误: {str(e)}"
        )
