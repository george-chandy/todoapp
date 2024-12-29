from sqlalchemy import Column, Date, ForeignKey, Integer, String, Enum,ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship
from schema.schema import TaskStatus

class Tasklist(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    task_user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date)
    todolist = Column(String)
    
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)

    users = relationship("Users", backpopulates="tasks")

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
