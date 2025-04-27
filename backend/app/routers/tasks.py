from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskUpdateStatus, Task
from app.db.session import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    raise NotImplementedError("Task creation not implemented yet")


@router.get("/", response_model=list[Task])
def get_all_tasks(db: Session = Depends(get_db)):
    raise NotImplementedError("Get all tasks not implemented yet")
    

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError("Get task by ID not implemented yet")


@router.patch("/{task_id}", response_model=Task)
def update_task_status(task_id: int, status_update: TaskUpdateStatus, db: Session = Depends(get_db)):
    raise NotImplementedError("Update task status not implemented yet")


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError("Delete task not implemented yet")
