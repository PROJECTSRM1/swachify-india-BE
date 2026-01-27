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

from schemas.task_schema import (
    TaskCreate,
    TaskHistoryCreate
)

# =====================================================
# TASK SERVICES
# =====================================================

def create_task(
    db: Session,
    payload: TaskCreate,
    created_by: int
):
    """
    Create a new task and assign it to a user (student).
    created_by = logged-in user (admin / mentor / manager)
    """

    # -----------------------------
    # Validate Project
    # -----------------------------
    if not db.query(MasterProject).filter(
        MasterProject.id == payload.project_id,
        MasterProject.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project_id"
        )

    # -----------------------------
    # Validate Task Type
    # -----------------------------
    if not db.query(MasterTaskType).filter(
        MasterTaskType.id == payload.task_type_id,
        MasterTaskType.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_type_id"
        )

    # -----------------------------
    # Validate Status
    # -----------------------------
    if not db.query(MasterStatus).filter(
        MasterStatus.id == payload.status_id,
        MasterStatus.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status_id"
        )

    # -----------------------------
    # Validate Assignee (Student)
    # -----------------------------
    if not db.query(UserRegistration).filter(
        UserRegistration.id == payload.user_id,
        UserRegistration.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assignee_user_id"
        )

    # -----------------------------
    # Create Task
    # -----------------------------
    task = Tasks(
        title=payload.title,
        description=payload.description,
        task_type_id=payload.task_type_id,
        project_id=payload.project_id,
        user_id=payload.user_id,  # 👈 assigned student
        reporting_manager_id=payload.reporting_manager_id,
        task_manager_id=payload.task_manager_id,
        status_id=payload.status_id,
        due_date=payload.due_date,
        efforts_in_days=payload.efforts_in_days,
        created_by=created_by
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task_status(
    db: Session,
    task_id: int,
    status_id: int,
    modified_by: int
):
    """
    Update task status
    """

    task = db.query(Tasks).filter(
        Tasks.id == task_id,
        Tasks.is_active == True
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Validate Status
    if not db.query(MasterStatus).filter(
        MasterStatus.id == status_id,
        MasterStatus.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status_id"
        )

    task.status_id = status_id
    task.modified_by = modified_by

    db.commit()
    db.refresh(task)
    return task


# =====================================================
# TASK HISTORY / RATING SERVICES
# =====================================================

def add_task_rating(
    db: Session,
    payload: TaskHistoryCreate,
    created_by: int
):
    """
    Add rating for a completed task
    Used for student performance & leaderboard
    """

    # -----------------------------
    # Validate Task
    # -----------------------------
    task = db.query(Tasks).filter(
        Tasks.id == payload.task_id,
        Tasks.is_active == True
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_id"
        )

    # -----------------------------
    # Ensure rating user is task assignee
    # -----------------------------
    if task.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not the assignee of this task"
        )

    # -----------------------------
    # Validate Rating Range
    # -----------------------------
    if payload.rating < 1 or payload.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    # -----------------------------
    # Insert Task History
    # -----------------------------
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


def get_task_history_by_task(
    db: Session,
    task_id: int
):
    """
    Get rating history for a task
    """

    return (
        db.query(TaskHistory)
        .filter(
            TaskHistory.task_id == task_id,
            TaskHistory.is_active == True
        )
        .order_by(TaskHistory.created_date.desc())
        .all()
    )


