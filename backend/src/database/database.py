"""Database connection module"""

import os
from dotenv import load_dotenv
import psycopg2

# Load env variables
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )

        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS prompts (
                    id SERIAL PRIMARY KEY,
                    prompt_name VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            self.conn.commit()

    def save_prompt(self, prompt_name, content):
        """
        Save a prompt to the database
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prompts (prompt_name, content)
                VALUES (%s, %s)
                RETURNING id
                """,
                (prompt_name, content),
            )
            prompt_id = cur.fetchone()[0]
            self.conn.commit()
            return prompt_id

    def get_prompt(self, prompt_id):
        """
        Retrieve a prompt by ID
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, prompt_name, content, created_at
                FROM prompts
                WHERE id = %s
                """,
                (prompt_id,),
            )
            result = cur.fetchone()
            if result:
                return {
                    "id": result[0],
                    "prompt_name": result[1],
                    "content": result[2],
                    "created_at": result[3],
                }
            return None

    def list_prompts(self):
        """
        List all prompts
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, prompt_name, content, created_at
                FROM prompts
                ORDER BY created_at DESC
                """
            )
            prompts = cur.fetchall()
            return [
                {"id": p[0], "prompt_name": p[1], "content": p[2], "created_at": p[3]}
                for p in prompts
            ]

    def delete_prompt(self, prompt_id):
        """
        Delete a prompt from the database
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM prompts WHERE id = %s", (prompt_id,))
            self.conn.commit()
            return cur.rowcount > 0

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()
