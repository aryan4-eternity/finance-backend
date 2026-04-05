import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-not-for-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
settings = Settings()