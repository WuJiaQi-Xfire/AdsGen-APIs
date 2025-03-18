import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    azure_gpt_api_key: str = os.getenv("AZURE_GPT_API_KEY")
    azure_gpt_api_endpoint: str = os.getenv("AZURE_GPT_API_ENDPOINT")
    sd_base_url: str = os.getenv("SD_BASE_URL")
    allowed_origins: list = ["http://localhost:8080"]

    class Config:
        env_file = ".env"

settings = Settings()