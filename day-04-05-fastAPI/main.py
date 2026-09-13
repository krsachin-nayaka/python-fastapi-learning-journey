from fastapi import FastAPI
from pydantic import BaseModel


# Request Model
class UserCreate(BaseModel):
    name: str
    age: int
    mobile: int
    password: str


# Response Model
class UserResponse(BaseModel):
    name: str
    age: int
    mobile: int


app = FastAPI()


@app.post("/create", response_model=UserResponse)
def create_user(user: UserCreate):
    return user
