from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI()

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.todo)

tasks: List[Task] = []
next_task_id = 1

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    """Return a list of all tasks."""
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate):
    """Create a new task."""
    global next_task_id
    new_task = Task(
        id=next_task_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        created_at=datetime.utcnow(),
    )
    tasks.append(new_task)
    next_task_id += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Return a single task by ID."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    """Update a task by its ID."""
    for task in tasks:
        if task.id == task_id:
            if task_data.title:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.status:
                task.status = task_data.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)