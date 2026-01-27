from fastapi import APIRouter,HTTPException, Depends, Query, Header
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.application_schema import ApplicationUpdateRequest,ApplicationReviewResponse
from services.application_service import get_application_review, update_application
from schemas.application_schema import TrendingStudentResponse
from services.application_service import get_trending_students
###
from schemas.application_schema import (
    JobOpeningCreateSchema,
    JobOpeningResponseSchema
)

from services.application_service import (
    create_job_opening,
    get_job_openings
)



router = APIRouter(prefix="/internship/application", tags=["Internship Application"])

#internship added

@router.post("")
def add_job_opening(
    payload: JobOpeningCreateSchema,
    db: Session = Depends(get_db),
    # user_id: int = Header(...)
):
   
    return create_job_opening(db, payload)



@router.get("")
def get_internships(
    create_job_id: int | None = Query(
        default=None,
        description="Fetch single internship by job id"
    ),
    category_id: int | None = Query(
        default=None,
        description="Filter internships by category id"
    ),
    db: Session = Depends(get_db)
):
    data = get_job_openings(
        db=db,
        job_id=create_job_id,
        category_id=category_id
    )

    return {
        "status": True,
        "data": data
    }



@router.get("/trending", response_model=List[TrendingStudentResponse])
def trending_students(db: Session = Depends(get_db)):
    return get_trending_students(db)

@router.get(
    "/{user_id}",
    response_model=ApplicationReviewResponse
)
def get_application(user_id: int):
    data = get_application_review(user_id)

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    return data


@router.put("/{user_id}")
def update_application_api(user_id: int, payload: ApplicationUpdateRequest):
    update_application(user_id, payload)
    return {"message": "Updated successfully"}



