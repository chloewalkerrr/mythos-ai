"""
Database connection setup
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from models.config import settings

# Database configuration
DB_USER = settings.db_user
DB_PASSWORD = settings.db_password.get_secret_value()
DB_HOST = settings.db_host
DB_PORT = settings.db_port
DB_NAME = settings.db_name

# Build database connection URL
if DB_PASSWORD:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
