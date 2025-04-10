'''
Database initialization
'''
import logging
import sys
import os
from pathlib import Path
from sqlalchemy import inspect, text, create_engine
from sqlalchemy.exc import SQLAlchemyError

# 将项目根目录添加到Python的导入路径中
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量中获取数据库配置
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB_Test", "testdb")

# 构建同步数据库URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
# 创建同步数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def init_db() -> None:
    """
    初始化数据库，如果user表不存在则创建
    """
    try:
        # 检查user表是否存在
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if "user" not in tables:
            logger.info("User表不存在，需要创建")
        else:
            logger.info("User表已存在，跳过初始化")

    except SQLAlchemyError as e:
        logger.error("Database initialization error: %s", e)
        raise

def check_db_connected() -> bool:
    """
    检查数据库连接是否正常
    """
    try:
        # 使用engine.connect()，这样可以确保正确处理事务
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error("Database connection error: %s", e)
        return False

if __name__ == "__main__":
    logger.info("正在检查数据库连接...")
    if check_db_connected():
        logger.info("数据库连接正常，开始初始化数据库...")
        init_db()
        logger.info("数据库初始化完成")
    else:
        logger.error("无法连接到数据库，请检查数据库配置")
