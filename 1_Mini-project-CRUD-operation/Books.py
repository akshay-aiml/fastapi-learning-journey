"""
Mini Project: Books CRUD API

Concepts Covered:
- GET, POST, PUT, DELETE
- Path Parameters
- Query Parameters
- Filtering
- Request Validation
- Pydantic Models
- HTTPException
- Clean API Structure
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Books CRUD API",
    description="Beginner-friendly CRUD API using FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# Pydantic Models
# --------------------------------------------------

class Book(BaseModel):

    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Book title"
    )

    author: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Author name"
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Book category"
    )


# --------------------------------------------------
# Fake Database
# --------------------------------------------------

BOOKS: List[dict] = [
    {
        "title": "Title One",
        "author": "Author One",
        "category": "science"
    },
    {
        "title": "Title Two",
        "author": "Author Two",
        "category": "science"
    },
    {
        "title": "Title Three",
        "author": "Author Three",
        "category": "history"
    },
    {
        "title": "Title Four",
        "author": "Author Four",
        "category": "math"
    },
]


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Books CRUD API"
    }


# --------------------------------------------------
# GET All Books
# --------------------------------------------------

@app.get("/books")
def get_all_books():

    return {
        "success": True,
        "total_books": len(BOOKS),
        "books": BOOKS
    }


# --------------------------------------------------
# GET Book By Title
# --------------------------------------------------

@app.get("/books/{book_title}")
def get_book_by_title(book_title: str):

    for book in BOOKS:

        if book["title"].casefold() == book_title.casefold():              #casefold() convert uppercase into lower case

            return {
                "success": True,
                "book": book
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# --------------------------------------------------
# FILTER Books By Category
# --------------------------------------------------

@app.get("/books/category/")
def get_books_by_category(
    category: Optional[str] = Query(
        default=None,
        description="Filter books by category"
    )
):

    # Return all books if category not provided
    if category is None:

        return {
            "success": True,
            "books": BOOKS
        }

    filtered_books = [
        book
        for book in BOOKS
        if book["category"].casefold() == category.casefold()
    ]

    return {
        "success": True,
        "category": category,
        "total_books": len(filtered_books),
        "books": filtered_books
    }


# --------------------------------------------------
# CREATE Book
# --------------------------------------------------

@app.post("/books")
def create_book(new_book: Book):

    # Check duplicate title
    for book in BOOKS:

        if book["title"].casefold() == new_book.title.casefold():

            raise HTTPException(
                status_code=400,
                detail="Book already exists"
            )

    BOOKS.append(new_book.model_dump())

    return {
        "success": True,
        "message": "Book added successfully",
        "book": new_book
    }


# --------------------------------------------------
# UPDATE Full Book (PUT)
# --------------------------------------------------

@app.put("/books/{book_title}")
def update_book(
    book_title: str,
    updated_book: Book
):

    for index, book in enumerate(BOOKS):

        if book["title"].casefold() == book_title.casefold():

            BOOKS[index] = updated_book.model_dump()

            return {
                "success": True,
                "message": "Book updated successfully",
                "book": BOOKS[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# --------------------------------------------------
# DELETE Book
# --------------------------------------------------

@app.delete("/books/{book_title}")
def delete_book(book_title: str):

    for index, book in enumerate(BOOKS):

        if book["title"].casefold() == book_title.casefold():

            deleted_book = BOOKS.pop(index)

            return {
                "success": True,
                "message": "Book deleted successfully",
                "deleted_book": deleted_book
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )