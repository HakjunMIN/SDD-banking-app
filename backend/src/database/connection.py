"""
Database Connection and Session Management
SQLite database setup for Banking App
"""

import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

logger = logging.getLogger(__name__)

# Create SQLite engine
# Echo=True for development to see SQL queries
logger.info(f"Creating database engine with URL: {settings.database.url}")
engine = create_engine(
    settings.database.url,
    echo=settings.database.echo,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for database models
Base = declarative_base()

# Database dependency for FastAPI
def get_db():
    """
    Database session dependency for FastAPI routes
    Yields a database session and ensures it's closed after use
    """
    logger.debug("Creating database session")
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session yielded successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        db.close()

# Create all tables
def create_tables():
    """Create all database tables using SQLAlchemy models (only if they don't exist)"""
    logger.info("Checking and creating database tables if needed...")
    
    try:
        # Import models to ensure they are registered with Base
        from ..models import database_models
        logger.info("Database models imported successfully")
        
        # Check existing tables first
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables: {existing_tables}")
        
        # Get expected tables from metadata
        expected_tables = [table.name for table in Base.metadata.tables.values()]
        logger.info(f"Expected tables: {expected_tables}")
        
        # Check if all tables exist
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        
        if missing_tables:
            logger.info(f"Missing tables detected: {missing_tables}")
            logger.info("Creating missing database tables...")
            # Create all tables (only missing ones will be created)
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully!")
            
            # Verify tables were created
            new_tables = inspector.get_table_names()
            logger.info(f"Tables after creation: {new_tables}")
        else:
            logger.info("All required tables already exist. Skipping table creation.")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

# Drop all tables (for testing/development)
def drop_tables():
    """Drop all database tables"""
    logger.info("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped successfully")