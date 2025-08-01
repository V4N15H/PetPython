from fastapi import APIRouter
from repository import TaskRepository
from schemas import STaskAdd, STaskId, STask

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)

@router.post("")
async def add_task(task: STaskAdd) -> STaskId:
    new_task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": new_task_id}

@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks
