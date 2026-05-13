
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(
    title="Reusable Dependency API",
    description="Learn reusable dependencies using Depends in FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# User Schema
# --------------------------------------------------

class User(BaseModel):
    name: str
    role: str


# --------------------------------------------------
# Reusable Dependency
# --------------------------------------------------

def get_current_user() -> User:
    """
    Simulates fetching logged-in user data.
    """

    return User(
        name="Ravi",
        role="AI Engineer"
    )


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Reusable Dependency API"
    }


# --------------------------------------------------
# Dashboard API
# --------------------------------------------------

@app.get("/dashboard")
def dashboard(
    user: User = Depends(get_current_user)
):
    """
    Dashboard endpoint using reusable dependency.
    """

    return {
        "success": True,
        "message": f"Welcome {user.name}",
        "role": user.role
    }


# --------------------------------------------------
# Settings API
# --------------------------------------------------

@app.get("/settings")
def settings(
    user: User = Depends(get_current_user)
):
    """
    Settings endpoint using reusable dependency.
    """

    return {
        "success": True,
        "message": "User settings page",
        "user": user
    }