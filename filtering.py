from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(
    title="Product Filtering API",
    description="Learn filtering using query parameters in FastAPI",
    version="1.0.0"
)

# --------------------------------------------------
# Product Schema
# --------------------------------------------------

class Product(BaseModel):
    id: int
    name: str
    category: str


# --------------------------------------------------
# Fake Database
# --------------------------------------------------

products_db = [
    {"id": 1, "name": "iPhone 15", "category": "mobile"},
    {"id": 2, "name": "Samsung S24", "category": "mobile"},
    {"id": 3, "name": "MacBook Pro", "category": "laptop"},
    {"id": 4, "name": "Dell XPS", "category": "laptop"},
    {"id": 5, "name": "AirPods", "category": "accessories"},
]


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Product Filtering API"
    }


# --------------------------------------------------
# Get All Products / Filter Products
# --------------------------------------------------

@app.get("/products")
def get_products(
    category: Optional[str] = Query(
        default=None,
        description="Filter products by category"
    )
):
    """
    Get all products or filter by category.
    """

    # Return all products
    if category is None:
        return {
            "success": True,
            "total_products": len(products_db),
            "products": products_db
        }

    # Filter products (case-insensitive)
    filtered_products = [
        product
        for product in products_db
        if product["category"].lower() == category.lower()
    ]

    # No products found
    if not filtered_products:
        return {
            "success": False,
            "message": f"No products found for category: {category}"
        }

    return {
        "success": True,
        "filter": category,
        "total_products": len(filtered_products),
        "products": filtered_products
    }


# --------------------------------------------------
# Get Single Product
# --------------------------------------------------

@app.get("/products/{product_id}")
def get_single_product(product_id: int):

    for product in products_db:

        if product["id"] == product_id:
            return {
                "success": True,
                "product": product
            }

    return {
        "success": False,
        "message": "Product not found"
    }