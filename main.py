from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    product_name: str


@app.get("/")
def read():
    return{"message": "Hello my name is akshay"}

# Path Parameter
@app.get("/items/{item_id}/user_id/{user_id}")
def read_items(item_id: int, user_id: int):
    return {"item_id": item_id, "user_id": user_id}


# @app.get("/product_name/{product_name}")
# def product_name(product_name:str):
#     product = Product(product_name=product_name)
#     return {"product_name": product.product_name}

# static route
@app.get("/info")
def info():
    return {"msg" : "wellcome to the world of AI"}

# Dynamic Route
@app.get("/hellow/{name}")
def greet(name: str):
    return {"message": f"Hello {name}"}

# query Parameter
@app.get("/users")
def users(user_id: int, user_name: str):
    return {
        "user_id": user_id,
        "user_name": user_name
    }

# Request body
# class User(BaseModel):
#     username: str
#     user_id: int
#
# @app.post("/Users")
# def users_data(user_id :User, user_name :User  ):
#     return {"user_id":user_id, "user_name":user_name}

class User(BaseModel):
    username: str
    user_id: int

@app.post("/users")
def users_data(user: User):
    return {
        "user_id": user.user_id,
        "user_name": user.username
    }
