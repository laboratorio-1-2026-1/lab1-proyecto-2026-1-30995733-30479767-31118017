from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "CLAVE_QUE_NO_ES_SECRETA"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://postgres:clave@localhost:5432/db"
    
    class Config:
        env_file = ".env"
        
settings = Settings()