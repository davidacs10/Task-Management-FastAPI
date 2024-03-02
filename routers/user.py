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
    return search(id)

@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):

    for existing_user in users_list:
        if existing_user.id == user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Ya existe un usuario con ese ID")
    
    users_list.append(user)
    return user


# Search
def search(id: int):
    for user in users_list:
        if user.id == id:
            return user
        
    return {"error": "User not found"}

    # users = filter(lambda user: user.id == id, list_user)
    # try:
    #     return list(users)[0]
    # except:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="User not found",
    #                         headers={"404":"Not Found"})