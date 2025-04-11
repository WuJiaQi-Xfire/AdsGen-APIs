"""Script to create user and prompts tables in testdb database"""

import os
import psycopg2
from dotenv import load_dotenv

# 加载环境变量
env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
load_dotenv(dotenv_path=env_path)

# 数据库连接参数 - 使用Database-Victor的参数
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_SERVER")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB_Test")  # 使用testdb数据库
def create_tables():
    """创建user和prompts表"""
    try:
        # 打印连接参数（不包括密码）
        print(f"连接参数: database={DB_NAME}, user={DB_USER}, host={DB_HOST}, port={DB_PORT}")
        
        # 确保密码不为空
        if not DB_PASSWORD:
            print("警告: 数据库密码为空!")
        
        # 连接到testdb数据库
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        
        # 创建cursor
        with conn.cursor() as cur:
            # 检查user schema是否存在，如果不存在则创建
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'user';")
            if not cur.fetchone():
                print("创建user schema...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS \"user\";")
            
            # 检查prompt schema是否存在，如果不存在则创建
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'prompt';")
            if not cur.fetchone():
                print("创建prompt schema...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS prompt;")
            
            # 检查user schema中的users表是否存在
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'user' 
                    AND table_name = 'users'
                );
            """)
            if cur.fetchone()[0]:
                print("user.users表已存在，跳过创建")
            else:
                # 在user schema中创建users表
                print("创建user.users表...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS "user".users (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        hashed_password VARCHAR(255) NOT NULL,
                        full_name VARCHAR(255),
                        is_active BOOLEAN DEFAULT TRUE,
                        is_superuser BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE
                    );
                """)
            
            # 检查prompt schema中的prompts表是否存在
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'prompt' 
                    AND table_name = 'prompts'
                );
            """)
            if cur.fetchone()[0]:
                print("prompt.prompts表已存在，跳过创建")
            else:
                # 在prompt schema中创建prompts表
                print("创建prompt.prompts表...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS prompt.prompts (
                        id SERIAL PRIMARY KEY,
                        prompt_name VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            
            # 提交事务
            conn.commit()
            print("成功创建users和prompts表！")
    
    except Exception as e:
        print(f"创建表时出错: {e}")
    
    finally:
        # 关闭连接
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables()
