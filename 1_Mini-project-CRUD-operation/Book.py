
from typing import List
from fastapi import FastAPI,HTTPException,Path,Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Book API",
    description="Production-style FastAPI CRUD project",
    version="2.0.0"
)

# ==================================================
# Internal Database Model
# ==================================================

class Book:
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_year: int
    ):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


# ==================================================
# Request Schema
# ==================================================

class BookRequest(BaseModel):

    title: str = Field(...,min_length=3,max_length=100)

    author: str = Field(...,min_length=2,max_length=50)

    description: str = Field(...,min_length=5,max_length=200)

    rating: int = Field(...,gt=0,lt=6)

    published_year: int = Field(...,gt=1999,lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Mastery",
                "author": "Akshay",
                "description": "Complete FastAPI backend guide",
                "rating": 5,
                "published_year": 2026
            }
        }
    }


# ==================================================
# Response Schema
# ==================================================

class BookResponse(BaseModel):

    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    class Config:
        from_attributes = True      #from_attributes = True allows Pydantic models to read data from object attributes instead of only dictionaries.
                                      # normal python object into json response (Read data from object attributes and convert it into JSON.)

# ==================================================
# Fake Database
# ==================================================

BOOKS: List[Book] = [
    Book(
        1,
        "FastAPI Pro",
        "Akshay",
        "Advanced FastAPI Guide",
        5,
        2026
    ),

    Book(
        2,
        "Master Python",
        "shiva",
        "Deep Python Concepts",
        4,
        2025
    ),
    Book(
        3,
        "Master Machine Learning",
        "soha",
        "Deep ML Concepts",
        4,
        2024
    ),
]


# ==================================================
# Helper Functions
# ==================================================

def generate_book_id() -> int:

    if not BOOKS:
        return 1

    return BOOKS[-1].id + 1


def find_book(book_id: int) -> Book:

    for book in BOOKS:

        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
async def home():

    return {
        "message": "Welcome to Book API"
    }


# ==================================================
# Get All Books
# ==================================================

@app.get(
    "/books",
    response_model=List[BookResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_books():

    return BOOKS


# ==================================================
# Filter Books By Rating
# ==================================================

@app.get(
    "/books/by-rating",
    response_model=List[BookResponse]
)
async def get_books_by_rating(
    rating: int = Query(...,gt=0,lt=6,description="Filter books by rating")
):

    return [
        book
        for book in BOOKS
        if book.rating == rating
    ]


# ==================================================
# Filter Books By Year
# ==================================================

@app.get(
    "/books/by-year",
    response_model=List[BookResponse]
)
async def get_books_by_year(
    year: int = Query(...,gt=1999,lt=2031,description="Filter books by published year")
):
    return [
        book
        for book in BOOKS
        if book.published_year == year
    ]


# ==================================================
# Get Single Book
# ==================================================

@app.get(
    "/books/{book_id}",
    response_model=BookResponse
)
async def get_book(
    book_id: int = Path(
        ...,
        gt=0,
        description="Book ID"
    )
):

    return find_book(book_id)


# ==================================================
# Create Book
# ==================================================

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    book_request: BookRequest
):

    new_book = Book(
        id=generate_book_id(),
        title=book_request.title,
        author=book_request.author,
        description=book_request.description,
        rating=book_request.rating,
        published_year=book_request.published_year
    )

    BOOKS.append(new_book)

    return new_book


# ==================================================
# Update Book
# ==================================================

@app.put(
    "/books/{book_id}",
    response_model=BookResponse
)
async def update_book(
    book_id: int,
    updated_book: BookRequest
):

    existing_book = find_book(book_id)

    existing_book.title = updated_book.title
    existing_book.author = updated_book.author
    existing_book.description = updated_book.description
    existing_book.rating = updated_book.rating
    existing_book.published_year = updated_book.published_year

    return existing_book


# ==================================================
# Delete Book
# ==================================================

@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: int = Path(...,gt=0)
):

    existing_book = find_book(book_id)

    BOOKS.remove(existing_book)

    return