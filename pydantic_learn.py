from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class address(BaseModel):
    state: str
    city:str

class User(BaseModel):
    name: str
    age: int
    address: address # model can contain other model


@app.post("/users")
def create_user(user: User):
    return user

# nested model
