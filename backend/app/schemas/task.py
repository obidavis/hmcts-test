from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskBase(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    status: TaskStatus = Field(..., description="Status of the task (pending, in_progress, completed, failed)")
    due_date: datetime = Field(..., description="Due date of the task in ISO format")

class TaskCreate(TaskBase):
    pass 

class TaskUpdateStatus(BaseModel):
    status: TaskStatus = Field(..., description="New status of the task")

class Task(TaskBase):
    id: int = Field(..., description="Unique identifier of the task")
    
