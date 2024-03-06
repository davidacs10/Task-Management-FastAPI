from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
<<<<<<< HEAD
    time_remaining: Optional[timedelta] = None
=======
    remaining_time: Optional[timedelta] = None
>>>>>>> e038e1426ddece4a746c1bedaa0331ee33432234
    status: str



router = APIRouter(prefix="/tasks",
                   tags=["tasks"],
                   responses={status.HTTP_404_NOT_FOUND:{"message": "Not found"}})

task_list = [Task(id=1, title="Clean the room", description="Here goes task description", 
<<<<<<< HEAD
                  due_date="2024-03-07", status="Pending"),
             Task(id=2, title="Clean the kitchen", description="it should be clean", 
                  due_date="2024-03-08", status="Pending")]
=======
                  due_date=datetime(2024, 3, 10), status="Pending"),
             Task(id=2, title="Clean the kitchen", description="it should be clean", 
                  due_date=datetime(2024, 3, 8), status="Pending")]
>>>>>>> e038e1426ddece4a746c1bedaa0331ee33432234


@router.get("/")
async def task():
<<<<<<< HEAD
    for task in task_list:
        if task.due_date:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
            time_remaining = due_date - datetime.now()
            task.time_remaining = time_remaining
=======
    now = datetime.now()
    for task in task_list:
        task.remaining_time = task.due_date - now
>>>>>>> e038e1426ddece4a746c1bedaa0331ee33432234
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
