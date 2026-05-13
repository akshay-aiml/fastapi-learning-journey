
from typing import Literal
from fastapi import FastAPI, Query

app = FastAPI(
    title="Sorting API",
    description="Learn sorting using query parameters in FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# Fake Database
# --------------------------------------------------

items = [
    {"id": 1, "name": "Laptop", "price": 800},
    {"id": 2, "name": "Phone", "price": 500},
    {"id": 3, "name": "Tablet", "price": 300},
    {"id": 4, "name": "Monitor", "price": 200},
]


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Sorting API"
    }


# --------------------------------------------------
# Sorting API
# --------------------------------------------------

@app.get("/items")
def get_items(
    sort_by: Literal["id", "name", "price"] = Query(
        default="price",
        description="Field used for sorting"
    ),
    order: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sorting order"
    )
):
    """
    Sorting means arranging data in a specific order.

    Examples:
    /items?sort_by=price&order=asc
    /items?sort_by=name&order=desc
    """

    # Determine sorting direction
    reverse_sort = order == "desc"

    # Sort items dynamically
    sorted_items = sorted(
        items,
        key=lambda item: item[sort_by],
        reverse=reverse_sort
    )

    return {
        "success": True,
        "sorted_by": sort_by,
        "order": order,
        "total_items": len(sorted_items),
        "items": sorted_items
    }