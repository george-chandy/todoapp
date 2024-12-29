from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services import todoservices
from models import models
from schema import schema
from database.db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/tasks/", response_model=list[schema.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    tasks = await todoservices.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/tasks/{task_id}", response_model=schema.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await todoservices.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.post("/tasks/", response_model=schema.Task)
async def create_task(
    task: schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await todoservices.create_task(db=db, task=task)


@app.put("/tasks/{task_id}", response_model=schema.Task)
async def update_task(
    task_id: int, task: schema.Task, db: AsyncSession = Depends(get_db)
):
    db_task = await todoservices.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", response_model=schema.Task)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await todoservices.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.post("/users/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await todoservices.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return await todoservices.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schema.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await todoservices.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user