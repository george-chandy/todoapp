from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update

from models import models
from schema import schema


async def get_tasks(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Task)
        .options(selectinload(models.Task.user))
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_task(db: AsyncSession, user_id: int, task_id: int):
    result = await db.execute(
        select(models.Task)
        .options(selectinload(models.Task.user))
        .filter(
            models.Task.task_id == task_id, models.Task.user_id == user_id
        )
    )
    return result.scalars().first()


async def create_task(db: AsyncSession, user_id: int, task: schemas.TaskCreate):
    db_task = models.Task(user_id=user_id, **task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession, user_id: int, task_id: int, task: schemas.Task
):
    # Fetch the existing task with user details
    result = await db.execute(
        select(models.Task)
        .options(selectinload(models.Task.user))
        .filter(models.Task.task_id == task_id, models.Task.user_id == user_id)
    )
    db_task = result.scalars().first()

    if db_task:
        # Exclude user_id from the update as it's a foreign key
        for key, value in task.dict(exclude_unset=True, exclude={"user_id"}).items():
            setattr(db_task, key, value)

        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, user_id: int, task_id: int):
    db_task = await get_task(db, user_id, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.user_id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user