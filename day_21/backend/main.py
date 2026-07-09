from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from model import ToDoList
from schema import TaskInput, TasksResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tasks")
def create(task:TaskInput, db:Session = Depends(get_db)):
    new_task = ToDoList(task_title=task.title,description=task.description)
    db.add(new_task)
    db.commit()
    return {"message" : "Task Added Successfully"}

@app.get("/tasks")
def show_all(db:Session = Depends(get_db)):
    return db.query(ToDoList).all()

@app.get("/tasks/{id}")
def show_by_id(id:int, db:Session = Depends(get_db)):
    task =  db.query(ToDoList).filter_by(id=id).first()
    if task == None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/task/{id}")
def update(id:int, task:TaskInput,db:Session = Depends(get_db)):
    print(task)
    update_task = db.query(ToDoList).filter_by(id=id).first()
    if update_task == None:
        raise HTTPException(status_code=404, detail="Task not found")
    update_task.task_title = task.title
    update_task.description = task.description
    update_task.iscompleted = task.is_competed
    print(update_task)
    db.commit()
    return {"message" : "Task Updated Successfully"}


@app.delete("/task/{id}")
def delete(id:int,db:Session = Depends(get_db)):
    task = db.query(ToDoList).filter_by(id=id).first()
    if task == None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message" : "Task Deleted Successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

