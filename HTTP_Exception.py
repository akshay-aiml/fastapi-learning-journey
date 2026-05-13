
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI(
    title="HTTPException API",
    description="Learn how to handle errors using HTTPException in FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# User Schema
# --------------------------------------------------

class UserResponse(BaseModel):
    user_id: int
    name: str


# --------------------------------------------------
# Fake Database
# --------------------------------------------------

fake_users = {
    1: "tushar",
    2: "rameshwer",
    3: "swapnil"
}


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to HTTPException API"
    }


# --------------------------------------------------
# Get User By ID
# --------------------------------------------------

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(
        ...,
        gt=0,
        description="ID of the user"
    )
):
    """
    Get a single user by ID.

    Raises:
    - 404 → User not found
    - 422 → Invalid input validation
    """

    # Check if user exists
    if user_id not in fake_users:

        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

    # Return user data
    return {
        "user_id": user_id,
        "name": fake_users[user_id]
    }