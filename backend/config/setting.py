from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurationsclass for Login and JWT settings.
    """
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env" # Load environment variables from .env file

settings = Settings()
