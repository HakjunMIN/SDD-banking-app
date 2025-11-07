"""
Application Configuration (Legacy)
Settings for Banking App Backend - Use config/settings.py for new features
"""

import os


# Legacy configuration - kept for backward compatibility
class Settings:
    """Application settings configuration"""
    
    # Application
    APP_NAME: str = "Banking App Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./banking_app.db"
    DATABASE_PATH: str = "./banking_app.db"
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    def __init__(self):
        # Override with environment variables if available
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", str(self.PORT)))


# Global settings instance (legacy)
settings = Settings()