"""
Database configuration for SmartMama.

Creates:
- Database engine
- Database session
- Base class for SQLAlchemy models
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

# Initialize the PostgreSQL engine connection matrix
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Automatically tests connections before queries run
)

# Set up local session maker configurations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative base class mapping blueprints to active database tables
Base = declarative_base()
#star-sandra added this
def get_db():
    """
    Dependency generator function that yields a secure local database session wire 
    to API routers and guarantees it is cleanly closed after the request wraps up.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()