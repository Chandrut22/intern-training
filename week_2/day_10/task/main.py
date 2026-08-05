from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tasks(BaseModel):
    id : int
    title: str
    description: str

tasks = []


@app.post("/tasks")
def create(task:Tasks):
    tasks.append(Tasks(id = len(tasks)+1, title=task.title, description=task.description))
    return {"message": "Task added Successfully"}

@app.get("/tasks")
def show_all():
    return tasks

@app.get("/tasks/{id}")
def show_by_id(id:int):
    if(len(tasks) > id - 1): return tasks[id-1]
    raise HTTPException(status_code=404,detail="Task is not found. Please Give the correct task id")

@app.put("/task/{id}")
def update(id:int, task:Tasks):
    if(len(tasks) < id): raise HTTPException(status_code=404, detail="Task is not found. Please Give the correct task id")
    tasks.insert(id-1,Tasks(id = id, title=task.title, description=task.description))
    return {"message" : "Task updated Successfully"}

@app.delete("/task/{id}")
def delete(id:int):
    if(len(tasks) != 0):
        del tasks[id-1]
        return {"message" : "Task deleted Successfullt"}
    raise HTTPException(status_code=404, detail="Task is not found. Please Give the correct task id to delete")
