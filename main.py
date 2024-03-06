from fastapi import FastAPI
from routers import user, task

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)

# uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message":"Hello World"}