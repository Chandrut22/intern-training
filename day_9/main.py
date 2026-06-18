# API is stands for Application Programming Interface it enables the client and server to communicate and share data efficiency
# How it works: Request(Client) -> API -> Server(Get, process, response) -> API -> Client(Result)

# Client - Server Model is a fundamental networking architecture where tasks are distributed between "Clients" (Service request) and "Server" (Service Provider)
# Client initiate the communication by sending request and server process those requests to deliver the requested data or perform the necessary task
# Types of Architecture: (1) 2 - tier (2) 3 - tier

# HTTP - Hypertext Transfer protocol is foundational set of rules to allow the browser and server to communicate and exchange the data across the internet.
# How it work: Request -> Processing  -> Response

# HTTPS - Hypertext Transfer protocol secure is encrypted version of HTTP used to safely transmit data across the internet.
# How it work: Request -> Digital certificate(SSL/TLS) -> Verification(site authentication) -> Encryption

# Status Code Categories
# 1xx : Informational
# 2xx : Success
# 3xx : Redirectional
# 4xx : Client Error
# 5xx : Server Error

# Port 80 - HTTP                  
# Port 443 - HTTPS
# Port 25 - SMTP
# Port 53 - DNS

# HTTP methods is indicate the specific action to be performed on given web resource
# GET (Read) - used to retrive the data from the server
# POST (Create) - Submit the data to the server
# PUT (Update/Replace) - overwrite the entire target resources with new resources with new request content
# PATCH (Update) - applies the partical modification to resources instead of replacing the whole thing
# DELETE (Delete) - remove the data from the specific resources permanently from the server

# REST API (Representational state transfer) is architectural Sytle that allow different sofware application to communicate with each other over the internet
# Core concept: 
#   - Resource: any data or object that api provides the information
#   - URI: Uniform resource identifier unique web address used to target the specific resources
#   - Representation: the format used to deliver

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def welcome():
    return {"msg":"Hello Everyone Welcome to FastAPI"}

@app.get("/hello/{name}")
def greet(name):
    return {"msg":f"Hello {name}, Wish u have a nice day"}

# --------------------------------------------------------------------------------------------

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
    return {"message":"Task is not found. Please Give the correct task id"}

@app.put("/task/{id}")
def update(id:int, task:Tasks):
    tasks.insert(id-1,Tasks(id = id, title=task.title, description=task.description))
    return {"message" : "Task updated Successfully"}

@app.delete("/task/{id}")
def delete(id:int):
    if(len(tasks) != 0):
        del tasks[id-1]
        return {"message" : "Task deleted Successfullt"}
    return {"message":"Task is not found. Please Give the correct task id to delete"}
