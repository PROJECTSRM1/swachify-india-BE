from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# =====================================================
# TASK SCHEMAS
# =====================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    task_type_id: int = Field(..., description="Master task type ID")
    project_id: int = Field(..., description="Master project ID")

    # Student / Assignee
    user_id: int = Field(..., description="Student user ID")

    reporting_manager_id: Optional[int] = None
    task_manager_id: Optional[int] = None

    status_id: int = Field(..., description="Master status ID")

    due_date: Optional[date] = None
    efforts_in_days: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]

    task_type_id: int
    project_id: int

    user_id: int  # assignee
    reporting_manager_id: Optional[int]
    task_manager_id: Optional[int]

    status_id: int
    due_date: Optional[date]
    efforts_in_days: Optional[int]

    created_by: int
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    status_id: int = Field(..., description="New status ID")


# =====================================================
# TASK HISTORY / RATING SCHEMAS
# =====================================================

class TaskHistoryCreate(BaseModel):
    task_id: int = Field(..., description="Task ID")

    user_id: int = Field(..., description="Student (assignee) user ID")

    from_assignee_id: Optional[int] = Field(
        None, description="Previous assignee user ID"
    )
    to_assignee_id: Optional[int] = Field(
        None, description="New assignee user ID"
    )

    reporting_manager_id: Optional[int] = None

    comments: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")


class TaskHistoryResponse(BaseModel):
    id: int
    task_id: int
    user_id: int

    from_assignee_id: Optional[int]
    to_assignee_id: Optional[int]

    reporting_manager_id: Optional[int]
    comments: Optional[str]
    rating: int

    created_by: int
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


# =====================================================
# STUDENT PERFORMANCE / TOP PERFORMERS
# =====================================================

class StudentRatingResponse(BaseModel):
    user_id: int
    student_name: str

    skill: Optional[str]
    attendance_percentage: Optional[float]

    aggregate: Optional[str]
    degree: Optional[str]

    internship_status: Optional[str]
    rating: Optional[float]
