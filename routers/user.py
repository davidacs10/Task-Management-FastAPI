from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserIn(UserBase):
    password: str = ...

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

users_list = [UserIn(id=1, username="david01", password="123456", email="david11@dev.com"),
              UserIn(id=2, username="david02", password="654321", email="david10@dev.com"),]

router = APIRouter(prefix="/users")

@router.get("/")
async def user():
    return users_list

@router.get("/{id}")
async def user_by_id(id: int):
    return search_id(id)

@router.post("/", response_model=UserBase, status_code=201)
async def create_user(user: UserIn):
    if any(u.id == user.id for u in users_list):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Ya existe un usuario con ese ID")
    
    users_list.append(user)
    return user

@router.put("/")
async def update_user(user: UserIn):

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="ID Not found",
                        headers={"404":"Not found"})
        
@router.delete("/{id}")
async def delete_user(id: int):
    
    for index, user in enumerate(users_list):
        if user.id == id:
            del users_list[index]
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                                detail="User successfully deleted",
                                headers={"202":"User deleted"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found",
                        headers={"404":"User not found"})

# Search
def search_id(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}