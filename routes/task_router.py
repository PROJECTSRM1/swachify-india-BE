from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services.tasks_service import (
   
    add_task_rating,
    get_task_history_by_task
)
from schemas.task_schema import (
    
    
    TaskHistoryCreate,
    TaskHistoryResponse,
    StudentRatingResponse
)

router = APIRouter(prefix="/api/tasks",tags=["Student/Tasks"])





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


