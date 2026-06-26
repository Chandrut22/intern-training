from pydantic import BaseModel

class TaskInput(BaseModel):
    title: str
    description: str
    is_competed: bool = False


class TasksResponse(BaseModel):
    id:int
    title:str
    description:str
    is_competed: bool

