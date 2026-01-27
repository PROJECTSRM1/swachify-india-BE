from fastapi import APIRouter,HTTPException, Depends, Query, Header
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db

from schemas.application_schema import (
    ApplicationUpdateRequest,
    ApplicationReviewResponse,
    TrendingStudentResponse,
    JobOpeningCreateSchema,
    JobOpeningResponseSchema,
    MasterJobResponse,
    JobSuccessResponse
)

from services.application_service import (
    get_application_review,
    update_application,
    get_trending_students,
    create_job_opening,
    get_job_openings,
    fetch_master_job,
    fetch_success_ui_by_job_id
)

router = APIRouter(prefix="/internship/application", tags=["Internship Api"])


# ---------------------------
# POST JOB OPENING
# ---------------------------
@router.post("")
def add_job_opening(
    payload: JobOpeningCreateSchema,
    db: Session = Depends(get_db),
):
    return create_job_opening(db, payload)


# ---------------------------
# GET INTERNSHIPS LIST
# ---------------------------
@router.get("")
def get_internships(
    create_job_id: int | None = Query(None, description="Fetch single internship by job id"),
    category_id: int | None = Query(None, description="Filter internships by category id"),
    db: Session = Depends(get_db)
):
    data = get_job_openings(db=db, job_id=create_job_id, category_id=category_id)

    return {
        "status": True,
        "data": data
    }


# ---------------------------
# TRENDING STUDENTS
# ---------------------------
@router.get("/trending", response_model=List[TrendingStudentResponse])
def trending_students(db: Session = Depends(get_db)):
    return get_trending_students(db)


# ---------------------------
# ✅ YOUR INTERNSHIP API — MUST BE ABOVE DYNAMIC ROUTES
# ---------------------------
@router.get("/internship")
def get_job_data(
    master_job_id: int | None = Query(None, description="Fetch Master Job Only"),
    job_id: int | None = Query(None, description="Fetch UI Success Card"),
    db: Session = Depends(get_db)
):
    # Prevent both params
    if master_job_id and job_id:
        raise HTTPException(
            status_code=400,
            detail="Provide ONLY ONE: master_job_id OR job_id"
        )

    # Case 1 — Master Job
    if master_job_id is not None:
        job = fetch_master_job(db, master_job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Master Job not found")
        return job

    # Case 2 — UI Success
    if job_id is not None:
        response = fetch_success_ui_by_job_id(db, job_id)
        if not response:
            raise HTTPException(status_code=404, detail="Job Opening not found")
        return response

    raise HTTPException(status_code=400, detail="Provide master_job_id OR job_id")


# ---------------------------
# APPLICATION REVIEW (DYNAMIC — MUST COME LAST)
# ---------------------------
@router.get("/{user_id}", response_model=ApplicationReviewResponse)
def get_application(user_id: int):
    data = get_application_review(user_id)

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    return data


@router.put("/{user_id}")
def update_application_api(user_id: int, payload: ApplicationUpdateRequest):
    update_application(user_id, payload)
    return {"message": "Updated successfully"}
