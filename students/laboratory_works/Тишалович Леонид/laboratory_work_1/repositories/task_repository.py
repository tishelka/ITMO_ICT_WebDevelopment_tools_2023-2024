from typing import List

from fastapi import HTTPException

from database import SessionLocal
from schemas import TaskCreate, TaskUpdate
from schemas import Task


class TaskRepository:
    @classmethod
    async def create(cls, data: TaskCreate):
        with SessionLocal() as session:
            task_dict = data.model_dump()

            if task_dict:
                try:
                    task = Task(**task_dict)
                    session.add(task)
                    session.commit()
                    return task
                except Exception as e:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail="Invalid data provided")

    @classmethod
    async def get_all(cls):
        with SessionLocal() as session:
            return session.query(Task).all()

    @classmethod
    async def get_by_id(cls, task_id: int):
        with SessionLocal() as session:
            return session.query(Task).filter(Task.id == task_id).first()

    @classmethod
    async def update(cls, task_id: int, task_data: TaskUpdate):
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                for field, value in task_data.dict().items():
                    setattr(task, field, value)
                session.commit()
                return task
            else:
                return None

    @classmethod
    async def delete(cls, task_id: int):
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return task
            else:
                return None

