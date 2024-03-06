from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    remaining_time: Optional[timedelta] = None
    status: str



router = APIRouter(prefix="/tasks",
                   tags=["tasks"],
                   responses={status.HTTP_404_NOT_FOUND:{"message": "Not found"}})

task_list = [Task(id=1, title="Clean the room", description="Here goes task description", 
                  due_date=datetime(2024, 3, 10), status="Pending"),
             Task(id=2, title="Clean the kitchen", description="it should be clean", 
                  due_date=datetime(2024, 3, 8), status="Pending")]


@router.get("/")
async def task():
    now = datetime.now()
    for task in task_list:
        task.remaining_time = task.due_date - now
    return task_list

@router.get("/{id}")
async def task_id(id: int):
    return search_task_by_id(id)

@router.post("/", response_model=Task, status_code=201)
async def create_task(task: Task):
    task_list.append(task)
    return task

@router.put("/")
async def update_task(task: Task):
    for index, saved_task in enumerate(task_list):
        if saved_task.id == task.id:
            task_list[index] = task
            return task
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")

@router.delete("/{id}")
async def delete_task(id: int):
    for index, saved_task in enumerate(task_list):
        if saved_task.id == id:
            del task_list[index]
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                                detail="Task deleted")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found")

# Search task by id
def search_task_by_id(id: int):
    tasks = filter(lambda task: task.id == id, task_list)

    try:
        return list(tasks)[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
