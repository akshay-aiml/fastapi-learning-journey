# Purpose: User CRUD APIs
# =========================================================


# =========================================================
# FASTAPI IMPORTS
# =========================================================

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Response,
    status
)

from sqlalchemy.orm import Session


# =========================================================
# LOCAL IMPORTS
# =========================================================

from database import engine
from Database_dependency import get_db

import models
import schemas


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="FastAPI CRUD Application",
    version="1.0.0"
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================
# Creates all tables automatically

models.Base.metadata.create_all(bind=engine)


# =========================================================
# CREATE USER
# =========================================================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)

def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Check if email already exists
    # -----------------------------------------------------

    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    # -----------------------------------------------------
    # Create new user object
    # -----------------------------------------------------

    db_user = models.User(
        name=user.name,
        email=user.email,
        age=user.age
    )


    # -----------------------------------------------------
    # Save user to database
    # -----------------------------------------------------

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# =========================================================
# GET ALL USERS
# =========================================================

@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)

def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(models.User).all()

    return users


# =========================================================
# UPDATE USER
# =========================================================

@app.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)

def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find user by ID
    # -----------------------------------------------------

    db_user = (
        db.query(models.User).filter(models.User.id == user_id).first()
    )


    # -----------------------------------------------------
    # Raise exception if user not found
    # -----------------------------------------------------

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    # -----------------------------------------------------
    # Update user data
    # -----------------------------------------------------

    db_user.name = user.name
    db_user.email = user.email
    db_user.age = user.age


    # -----------------------------------------------------
    # Save updated data
    # -----------------------------------------------------

    db.commit()
    db.refresh(db_user)

    return db_user


# =========================================================
# DELETE USER
# =========================================================

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find user by ID
    # -----------------------------------------------------

    db_user = (
        db.query(models.User).filter(models.User.id == user_id).first()
    )


    # -----------------------------------------------------
    # Raise exception if user not found
    # -----------------------------------------------------

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    # -----------------------------------------------------
    # Delete user
    # -----------------------------------------------------

    db.delete(db_user)
    db.commit()


    # -----------------------------------------------------
    # Return empty response
    # -----------------------------------------------------

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )