"""
Task Management API
Generated from SPEC.md by demos/01-spec-to-api/generate.py
"""

from datetime import datetime
from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Management API")

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

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
    status: TaskStatus = TaskStatus.todo


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------

_tasks: list[Task] = []
_next_id: int = 1


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    """Return a list of all tasks."""
    return _tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """Create a new task. Title is required. Status defaults to 'todo'."""
    global _next_id
    task = Task(
        id=_next_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        created_at=datetime.utcnow(),
    )
    _tasks.append(task)
    _next_id += 1
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Return a single task by ID. Returns 404 if not found."""
    for task in _tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    """Update title, description, or status of a task. Returns 404 if not found."""
    for i, task in enumerate(_tasks):
        if task.id == task_id:
            updated = task.model_copy(update=payload.model_dump(exclude_none=True))
            _tasks[i] = updated
            return updated
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID. Returns 204 on success, 404 if not found."""
    for i, task in enumerate(_tasks):
        if task.id == task_id:
            _tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
