"""
Environment Configuration
Enhanced configuration management with environment variables
"""

import os
from pathlib import Path
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Database configuration settings"""
    
    def __init__(self):
        self.url: str = os.getenv("DATABASE_URL", "sqlite:///./banking_app.db")
        self.path: str = os.getenv("DATABASE_PATH", "./banking_app.db")
        self.echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
        self.pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
        self.pool_timeout: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))


class ServerConfig:
    """Server configuration settings"""
    
    def __init__(self):
        self.host: str = os.getenv("HOST", "127.0.0.1")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.reload: bool = os.getenv("RELOAD", "true").lower() == "true"
        self.log_level: str = os.getenv("LOG_LEVEL", "info")
        self.workers: int = int(os.getenv("WORKERS", "1"))


class SecurityConfig:
    """Security and authentication settings"""
    
    def __init__(self):
        self.secret_key: str = os.getenv("SECRET_KEY", "banking-app-secret-key-change-in-production")
        self.allowed_origins: list = self._parse_allowed_origins()
        self.allowed_hosts: list = self._parse_allowed_hosts()
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
    
    def _parse_allowed_origins(self) -> list:
        """Parse allowed CORS origins from environment variable"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        return [origin.strip() for origin in origins_str.split(",") if origin.strip()]
    
    def _parse_allowed_hosts(self) -> list:
        """Parse allowed hosts from environment variable"""
        hosts_str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
        return [host.strip() for host in hosts_str.split(",") if host.strip()]


class APIConfig:
    """API configuration settings"""
    
    def __init__(self):
        self.v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
        self.page_size: int = int(os.getenv("API_PAGE_SIZE", "50"))
        self.max_page_size: int = int(os.getenv("API_MAX_PAGE_SIZE", "100"))
        self.timeout: int = int(os.getenv("API_TIMEOUT", "30"))


class LoggingConfig:
    """Logging configuration settings"""
    
    def __init__(self):
        self.level: str = os.getenv("LOG_LEVEL", "INFO").upper()
        self.format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file: Optional[str] = os.getenv("LOG_FILE")
        self.max_file_size: int = int(os.getenv("LOG_MAX_FILE_SIZE", "10485760"))  # 10MB
        self.backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))


class Settings:
    """Main application settings"""
    
    def __init__(self):
        # Application metadata
        self.app_name: str = "Banking App Backend"
        self.app_version: str = "0.1.0"
        self.debug: bool = os.getenv("DEBUG", "true").lower() == "true"
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        
        # Component configurations
        self.database = DatabaseConfig()
        self.server = ServerConfig()
        self.security = SecurityConfig()
        self.api = APIConfig()
        self.logging = LoggingConfig()
        
        # File paths
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() in ["development", "dev"]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() in ["production", "prod"]
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.environment.lower() in ["testing", "test"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()