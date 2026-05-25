# Purpose: Database Configuration
# =========================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================================================
# DATABASE URL
# =========================================================
# Format:
# database+dialect://username:password@host:port/database_name

DATABASE_URL = "mysql+pymysql://root:Akshay10@localhost:3306/fastapi_db"

# =========================================================
# SQLALCHEMY ENGINE
# =========================================================
# Engine manages the core database connection

engine = create_engine(
    DATABASE_URL,

    # Helps in debugging by printing SQL queries
    echo=True,

    # Prevents connection timeout issues
    pool_pre_ping=True
)

# =========================================================
# SESSION FACTORY
# =========================================================
# Creates independent database sessions
# One session per request

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# =========================================================
# BASE CLASS FOR MODELS
# =========================================================
# All ORM models/tables inherit from Base

Base = declarative_base()

