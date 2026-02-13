from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from models.generated_models import (
    Tasks,
    TaskHistory,
    MasterProject,
    MasterTaskType,
    MasterStatus,
    UserRegistration,
    t_vw_students_get_list
)
from schemas.task_schema import TaskHistoryCreate





def add_task_rating(db: Session,payload: TaskHistoryCreate,created_by: int):
    task = db.query(Tasks).filter(
        Tasks.id == payload.task_id,
        Tasks.is_active == True
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id"
        )
    if task.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not the assignee of this task"
        )
    if payload.rating < 1 or payload.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    history = TaskHistory(
        task_id=payload.task_id,
        user_id=payload.user_id,
        from_assignee_id=payload.from_assignee_id,
        to_assignee_id=payload.to_assignee_id,
        reporting_manager_id=payload.reporting_manager_id,
        comments=payload.comments,
        rating=payload.rating,
        created_by=created_by
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_task_history_by_task(db: Session,task_id: int):
    return (
        db.query(TaskHistory)
        .filter(
            TaskHistory.task_id == task_id,
            TaskHistory.is_active == True
        )
        .order_by(TaskHistory.created_date.desc())
        .all()
    )


