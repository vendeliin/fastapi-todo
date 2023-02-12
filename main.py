import uvicorn
from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

import models
from schemas import TaskSchema
from database import engine, SessionLocal
from models import Task


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return "welcome"

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create(request: TaskSchema, db: Session = Depends(get_db)):
    new_task = Task(body=request.body)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/all", status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
