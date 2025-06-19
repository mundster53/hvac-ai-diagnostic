"""
Configuration settings for HVAC AI Diagnostic backend.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Basic app info
    PROJECT_NAME: str = "HVAC AI Diagnostic"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Development settings
    DEBUG: bool = True
    
    # CORS settings - allows frontend to communicate with backend
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:8000",  # FastAPI docs
    ]
    
    # Database (we'll use SQLite for simplicity to start)
    DATABASE_URL: str = "sqlite:///./hvac_diagnostic.db"
    
    # Security
    SECRET_KEY: str = "hvac-development-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"


# Create settings instance
settings = Settings()