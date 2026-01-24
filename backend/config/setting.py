from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # = backend/


class Settings(BaseSettings):
    """
    Configurationsclass for Login and JWT settings.
    """
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    N8N_WEBHOOK_URL: str

    model_config = ConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )
    
settings = Settings()
