from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password: str

users_list = [User(id=1, username="david01", password="123456"),
              User(id=2, username="david02", password="654321"),]

router = APIRouter(prefix="/users")

@router.get("/")
async def user():
    return users_list

@router.get("/{id}")
async def user_by_id(id: int):
    return search_id(id)

@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):
    if type(search_id(user.id)) == User:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Ya existe un usuario con ese ID")
    
    users_list.append(user)
    return user


# Search
def search_id(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}