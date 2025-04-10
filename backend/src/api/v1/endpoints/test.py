from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

router = APIRouter()

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
