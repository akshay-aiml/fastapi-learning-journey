from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from typing import Annotated     # Annotated means adding extra information to a variable or parameter
app = FastAPI()

class UserResponse(BaseModel):
    user_id:int
    name : str
    email : str


@app.get("/users/1", response_model=UserResponse)
def get_user():
    return{
        "user_id" : 1,
        "name" : "tushar",
        "email" : "akshayy@123.com",
        "password" : "akki123"
    }

 #Dependency
def get_current_user():
    return{
     "user_name": "tushar",
     "role": "AIML Engineer"
    }

user_dependency = Annotated[dict, Depends(get_current_user)]

 #use Dependency in route
@app.get("/me")
def get_me(user:user_dependency):
    return {"massage": "user found","user": user}

# resue dependency
@app.get("/dashboard")
def get_me(user:user_dependency):
    return {"massage": f"well come to the Dashboard, {user['user_name']}",
            "role": user["role"]
    }