'''
Test database connection
'''
import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from main import app
from db.session import  engine

# add project root directory to Python import path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# create test client
client = TestClient(app)

# create a test route for testing database connection
@app.get("/test/db", tags=["Test"])
async def test_db_connection():
    ''' Test database connection '''
    try:
        # use SQLAlchemy to execute SQL queries directly
        async with engine.connect() as connection:
            # get PostgreSQL version
            version_result = await connection.execute(text("SELECT version()"))
            version_result = version_result.fetchone()
            
            # get current database name
            db_name_result = await connection.execute(text("SELECT current_database()"))
            db_name_result = db_name_result.fetchone()
            
            #  get current user
            user_result = await connection.execute(text("SELECT current_user"))
            user_result = user_result.fetchone()
            
            # get all table names
            tables_result = await connection.execute(
                text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """)
            )
            tables_result = tables_result.fetchall()
            
            tables = [table[0] for table in tables_result]
            
            return {
                "status": "success",
                "database": {
                    "version": version_result[0] if version_result else None,
                    "name": db_name_result[0] if db_name_result else None,
                    "user": user_result[0] if user_result else None,
                    "tables": tables
                }
            }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}"
        }
    except SyntaxError as e:
        return {
            "status": "error",
            "message": f"Syntax error: {str(e)}"
        }

# 测试函数
def test_db_api():
    """
    测试数据库API端点
    """
    response = client.get("/test/db")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "database" in data
    assert "version" in data["database"]
    assert "name" in data["database"]
    assert "user" in data["database"]
    assert "tables" in data["database"]
    
    # 验证数据库名称是否正确
    assert data["database"]["name"] == os.getenv("POSTGRES_DB_Test", "testdb")
    
    print("数据库连接测试成功!")
    print(f"数据库版本: {data['database']['version']}")
    print(f"数据库名称: {data['database']['name']}")
    print(f"数据库用户: {data['database']['user']}")
    print(f"数据库表: {data['database']['tables']}")

# 如果直接运行此文件，则执行测试
if __name__ == "__main__":
    test_db_api()
