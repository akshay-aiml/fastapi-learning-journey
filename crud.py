from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# CRUD
# Create  -> POST
# Read    -> GET
# Update  -> PUT / PATCH
# Delete  -> DELETE


# -----------------------------
# Pydantic Models
# -----------------------------

class User(BaseModel):
    id: int
    name: str
    age: int


class UserPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


# -----------------------------
# Dummy Database
# -----------------------------

dummy_DB = [
    {"id": 1, "name": "Akki", "age": 21},
    {"id": 2, "name": "Baka", "age": 22},
    {"id": 3, "name": "Raka", "age": 23},
]


# -----------------------------
# Root API
# -----------------------------

@app.get("/")
def read_root():
    return {"message": "CRUD Operations in FastAPI"}


# -----------------------------
# GET All Users
# -----------------------------

@app.get("/users")
def get_users():
    return dummy_DB


# -----------------------------
# GET Single User
# -----------------------------

@app.get("/users/{id}")
def get_single_user(id: int):

    for user in dummy_DB:
        if user["id"] == id:
            return user

    return {"error": "User not found"}


# -----------------------------
# CREATE User
# -----------------------------

@app.post("/users")
def create_user(user: User):

    # check duplicate ID
    for existing_user in dummy_DB:
        if existing_user["id"] == user.id:
            return {"error": "User ID already exists"}

    dummy_DB.append(user.model_dump())

    return {
        "message": "User created successfully",
        "user": user
    }


# -----------------------------
# PUT = Full Update
# -----------------------------

@app.put("/users/{id}")
def update_user(id: int, user: User):

    for index, existing_user in enumerate(dummy_DB):

        if existing_user["id"] == id:

            dummy_DB[index] = user.model_dump()

            return {
                "message": "User updated successfully",
                "user": dummy_DB[index]
            }

    return {"error": "User not found"}


# -----------------------------
# PATCH = Partial Update
# -----------------------------

@app.patch("/users/{id}")
def partial_update_user(id: int, user: UserPatch):

    for existing_user in dummy_DB:

        if existing_user["id"] == id:

            # update only provided fields
            if user.name is not None and user.name.strip() != "":
                existing_user["name"] = user.name

            if user.age is not None:
                existing_user["age"] = user.age

            return {
                "message": "User partially updated successfully",
                "user": existing_user
            }

    return {"error": "User not found"}


# -----------------------------
# DELETE User
# -----------------------------

@app.delete("/users/{id}")
def delete_user(id: int):

    for index, user in enumerate(dummy_DB):

        if user["id"] == id:

            deleted_user = dummy_DB.pop(index)

            return {
                "message": f"User {id} deleted successfully",
                "deleted_user": deleted_user
            }

    return {"error": "User not found"}