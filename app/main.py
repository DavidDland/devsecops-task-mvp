from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="DevSecOps Task Tracker",
    version="1.0.0",
    description="A tiny in-memory API for practicing Docker, CI/CD, and Kubernetes."
)

class TaskCreate(BaseModel):
    title: str

class Task(TaskCreate):
    id: int
    completed: bool = False

tasks: list[Task] = []
next_id = 1

@app.get("/")
def root():
    return {
        "message": "DevSecOps Task Tracker is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global next_id

    clean_title = task.title.strip()
    if not clean_title:
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    new_task = Task(id=next_id, title=clean_title, completed=False)
    next_id += 1
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return

    raise HTTPException(status_code=404, detail="Task not found")
