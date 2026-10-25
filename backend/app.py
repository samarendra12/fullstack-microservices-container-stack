import os
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Management Microservice",
    description="Enterprise REST API service backing the secure multi-tier application stack.",
    version="1.0.0",
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Detailed task description")

class Task(BaseModel):
    ID: str
    Title: str
    Description: str

# In-memory store (thread-safe for simple demo, replaceable by PostgreSQL via connection string)
task_db: List[dict] = [
    {
        "ID": "1",
        "Title": "Configure Azure Virtual Network Peering",
        "Description": "Establish non-transitive peering between Hub VNet and Spoke VNets.",
    },
    {
        "ID": "2",
        "Title": "Implement Shift-Left DevSecOps Gates",
        "Description": "Integrate Gitleaks, TFLint, and TFSec in Azure DevOps pipeline.",
    },
]

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "service": "task-management-backend", "version": "1.0.0"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return task_db

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    new_task = {
        "ID": str(uuid.uuid4())[:8],
        "Title": payload.title,
        "Description": payload.description or "",
    }
    task_db.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: str):
    global task_db
    initial_len = len(task_db)
    task_db = [t for t in task_db if t["ID"] != task_id]
    if len(task_db) == initial_len:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted", "id": task_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
