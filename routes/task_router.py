from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services.tasks_service import (
    create_task,
    update_task_status,
    add_task_rating,
    get_task_history_by_task
)
from schemas.task_schema import (
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskHistoryCreate,
    TaskHistoryResponse,
    StudentRatingResponse
)

router = APIRouter(prefix="/api/tasks",tags=["Student/Tasks"])

@router.post("/",response_model=TaskResponse,summary="Create Task")
def create_task_api(payload: TaskCreate,user_id: int = Query(..., description="Logged-in user ID"),db: Session = Depends(get_db)):
    return create_task(db=db, payload=payload, created_by=user_id)


@router.put("/{task_id}/status",response_model=TaskResponse,summary="Update Task Status")
def update_task_status_api(task_id: int,payload: TaskStatusUpdate,user_id: int = Query(..., description="Logged-in user ID"),db: Session = Depends(get_db)):
    return update_task_status(
        db=db,
        task_id=task_id,
        status_id=payload.status_id,
        modified_by=user_id
    )

@router.post("/rating",response_model=TaskHistoryResponse,summary="Add Task Rating")
def add_task_rating_api(payload: TaskHistoryCreate,user_id: int = Query(..., description="Logged-in user ID"),db: Session = Depends(get_db)):
    return add_task_rating(
        db=db,
        payload=payload,
        created_by=user_id
    )


@router.get("/{task_id}/history",response_model=List[TaskHistoryResponse],summary="Get Task History")
def get_task_history_api(task_id: int,db: Session = Depends(get_db)):
    return get_task_history_by_task(db=db, task_id=task_id)


