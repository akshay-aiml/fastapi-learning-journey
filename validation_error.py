
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Validation Error API",
    description="Learn automatic request validation in FastAPI using Pydantic",
    version="1.0.0"
)

# --------------------------------------------------
# User Schema
# --------------------------------------------------

class User(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User full name"
    )

    age: int = Field(
        ...,
        gt=0,
        lt=120,
        description="User age"
    )


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Validation Error API"
    }


# --------------------------------------------------
# Create User API
# --------------------------------------------------

@app.post("/users")
def create_user(user: User):
    """
    FastAPI automatically validates:
    - missing fields
    - wrong datatypes
    - invalid values
    """

    return {
        "success": True,
        "message": "User created successfully",
        "user": user
    }