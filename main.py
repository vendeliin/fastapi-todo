import uvicorn
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models
from schemas import TaskSchema
from database import engine, SessionLocal
from models import Task


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    return "welcome"

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create(request: TaskSchema, db: Session = Depends(get_db)):
    new_task = Task(body=request.body)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.delete("/delete-task/{id}")
def remove(request: TaskSchema, db: Session = Depends(get_db)):
    db.query(Task).filter(Task.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.get("/all", status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
