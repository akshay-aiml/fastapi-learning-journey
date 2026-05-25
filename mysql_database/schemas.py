# Purpose: Pydantic Schemas for User APIs
# =========================================================


# =========================================================
# PYDANTIC IMPORT
# =========================================================
# BaseModel is used for:
# - Request validation
# - Response validation
# - Data serialization

from pydantic import BaseModel, EmailStr


# =========================================================
# USER CREATE SCHEMA
# =========================================================
# Used when creating a new user
# (Request Body Schema)

class UserCreate(BaseModel):

    name: str
    email: EmailStr
    age: int


# =========================================================
# USER RESPONSE SCHEMA
# =========================================================
# Used for API responses
# Includes database-generated fields like ID

class UserResponse(UserCreate):

    id: int

    # -----------------------------------------------------
    # Pydantic Configuration
    # -----------------------------------------------------
    class Config:

        # Allows conversion from SQLAlchemy ORM model
        orm_mode = True