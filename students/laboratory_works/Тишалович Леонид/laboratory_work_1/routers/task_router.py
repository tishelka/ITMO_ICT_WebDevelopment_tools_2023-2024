from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repositories.task_repository import TaskRepository
from schemas import TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Задания"]
)


@router.post("/")
async def create_task(
        task: Annotated[TaskCreate, Depends()]
):
    await TaskRepository.create(task)


@router.get("/")
async def get_all_tasks() -> list[TaskCreate]:
    return await TaskRepository.get_all()


@router.get("/{task_id}")
async def get_task(task_id: int) -> TaskCreate:
    task = await TaskRepository.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate):
    updated_task = await TaskRepository.update(task_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    deleted_task = await TaskRepository.delete(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
