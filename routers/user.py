from fastapi import APIRouter
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

list_user = [User(username="david01", password="123456")]

router = APIRouter(prefix="/users")

@router.get("/")
async def user():
    return list_user