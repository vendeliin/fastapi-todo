from pydantic import BaseModel

class TaskSchema(BaseModel):
    body: str
