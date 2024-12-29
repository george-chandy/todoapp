from enum import Enum
from pydantic import BaseModel

class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class TaskBase(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass  # Inherit all fields from TaskBase

class Task(TaskBase):
    task_id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name : str

    

class UserCreate(UserBase):
    user_id : int
    hashed_password : str

class User(UserCreate):
    pass

    class Config:
        from_attributes = True

