
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Manager API",
    description="Beginner-friendly CRUD API using FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# Pydantic Models
# --------------------------------------------------

class Student(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Student name"
    )

    age: int = Field(
        ...,
        gt=0,
        lt=100,
        description="Student age"
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Student course"
    )


class StudentUpdate(BaseModel):

    age: int = Field(
        ...,
        gt=0,
        lt=100
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=50
    )


# --------------------------------------------------
# Fake Database
# --------------------------------------------------

STUDENTS: List[dict] = []


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to Student Manager API"
    }


# --------------------------------------------------
# CREATE Student
# --------------------------------------------------

@app.post("/students")
def add_student(student: Student):

    # Check duplicate student
    for existing_student in STUDENTS:

        if (
            existing_student["name"].casefold() == student.name.casefold()
        ):

            raise HTTPException(
                status_code=400,
                detail="Student already exists"
            )

    STUDENTS.append(student.model_dump())

    return {
        "success": True,
        "message": "Student added successfully",
        "student": student
    }


# --------------------------------------------------
# GET All Students
# --------------------------------------------------

@app.get("/students")
def get_all_students():

    return {
        "success": True,
        "total_students": len(STUDENTS),
        "students": STUDENTS
    }


# --------------------------------------------------
# GET Single Student
# --------------------------------------------------

@app.get("/students/{student_name}")
def get_student(student_name: str):

    for student in STUDENTS:

        if (
            student["name"].casefold() == student_name.casefold()
        ):

            return {
                "success": True,
                "student": student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# --------------------------------------------------
# UPDATE Student
# --------------------------------------------------

@app.put("/students/{student_name}")
def update_student(
    student_name: str,
    updated_data: StudentUpdate
):

    for student in STUDENTS:

        if (
            student["name"].casefold() == student_name.casefold()
        ):

            student["age"] = updated_data.age
            student["course"] = updated_data.course

            return {
                "success": True,
                "message": "Student updated successfully",
                "student": student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# --------------------------------------------------
# DELETE Student
# --------------------------------------------------

@app.delete("/students/{student_name}")
def delete_student(student_name: str):

    for index, student in enumerate(STUDENTS):

        if (
            student["name"].casefold() == student_name.casefold()
        ):

            deleted_student = STUDENTS.pop(index)

            return {
                "success": True,
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )