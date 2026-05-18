import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
  OPEN_API_KEY: str | None = os.getenv("OPEN_API_KEY")
  OPEN_AI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
  DATABASE_URL: str | None = os.getenv("DATABASE_URL")


settings = Settings()