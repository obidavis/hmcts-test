from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskUpdateStatus, Task
from app.models.tasks import DBTask
from app.db.session import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = DBTask(
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    return db_task


@router.get("/", response_model=list[Task])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(DBTask).all()
    

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task



@router.patch("/{task_id}", response_model=Task)
def update_task_status(task_id: int, status_update: TaskUpdateStatus, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.status = status_update.status
    db.commit()
    return db_task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None
