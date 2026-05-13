"""
Goal:
Learn how FastAPI automatically provides
database access using Depends().
"""

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(
    title="Database Dependency API",
    description="Learn database dependency injection using Depends in FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# Fake Database
# --------------------------------------------------

fake_users_db = [
    {"id": 1, "name": "RAJ"},
    {"id": 2, "name": "Ramesh"},
    {"id": 3, "name": "Raghunath"},
]


# --------------------------------------------------
# User Schema
# --------------------------------------------------

class User(BaseModel):
    id: int
    name: str


# --------------------------------------------------
# Database Dependency
# --------------------------------------------------

def get_db():
    """
    Simulates database connection setup.
    """

    db_connection = {
        "status": "Database connection successful",
        "database": "Fake PostgreSQL DB"
    }

    return db_connection


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to DB Dependency API"
    }


# --------------------------------------------------
# Get Users API
# --------------------------------------------------

@app.get("/users")
def get_users(
    db = Depends(get_db)
):
    """
    FastAPI automatically calls get_db()
    before executing this API.
    """

    return {
        "success": True,
        "message": "Users fetched successfully",
        "db_status": db,
        "users": fake_users_db
    }