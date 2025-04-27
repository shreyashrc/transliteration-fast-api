from pydantic import validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hindi/Marathi to Hinglish Transliteration API"
    API_PREFIX: str = "/api"
    
    DATABASE_URL: Optional[str] = "sqlite:///./transliteration.db"
    
    CORS_ORIGINS: Union[str, List[str]] = "*"
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()