from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime




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
