from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(
    title="HMCTS Task Tracker",
    description="Backend for HMCTS developer technical test",
    version="0.1.0",
)

app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the HMCTS Task Tracker API!"}