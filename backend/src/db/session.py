import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv(override=False)

# 从环境变量中获取数据库配置
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB_Test", "testdb")

# 构建数据库URL（使用异步驱动）
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# 创建异步数据库引擎
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 依赖函数，用于获取异步数据库会话
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话的依赖函数
    
    返回:
        AsyncGenerator: 异步数据库会话生成器
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
