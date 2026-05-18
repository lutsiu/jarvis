import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
  OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
  OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
  DATABASE_URL: str | None = os.getenv("DATABASE_URL")


settings = Settings()