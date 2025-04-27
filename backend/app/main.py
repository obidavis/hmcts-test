import datetime
from fastapi import FastAPI
from app.routers import tasks
from app.models.tasks import Base, DBTask
from app.db.session import engine, SessionLocal
from app.schemas.task import TaskStatus

app = FastAPI(
    title="HMCTS Task Tracker",
    description="Backend for HMCTS developer technical test",
    version="0.1.0",
)

app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the HMCTS Task Tracker API!"}

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if not db.query(DBTask).first():
            hello_world_task = DBTask(
                title="Hello World",
                description="A simple task to print 'Hello, World!'",
                status=TaskStatus.PENDING,
                due_date=datetime.datetime.now() + datetime.timedelta(days=7)
            ) 
            db.add(hello_world_task)
            db.commit()
            db.refresh(hello_world_task)
