from fastapi import FastAPI
from routers import user

app = FastAPI()

app.include_router(user.router)

# uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message":"Hello World"}