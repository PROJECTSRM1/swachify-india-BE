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
    delete_by_id,
    get_application_review,
    update_application,
    get_trending_students,
    create_job_opening,
    get_job_openings,
    fetch_master_job,
    fetch_success_ui_by_job_id
)
router = APIRouter(prefix="/internship/application", tags=["Internship Api"])

@router.post("")
def add_job_opening(payload: JobOpeningCreateSchema,db: Session = Depends(get_db),):
    return create_job_opening(db, payload)

@router.get("")
def get_application_internships(
    create_job_id: int | None = Query(None, description="Fetch single internship by job id"),
    category_id: int | None = Query(None, description="Filter internships by category id"),
    location_type_id: int | None = Query(None, description="Filter internships by location type id"),
    db: Session = Depends(get_db)
):
    data = get_job_openings(db=db, job_id=create_job_id, category_id=category_id, location_type_id=location_type_id)

    return {
        "status": True,
        "data": data
    }

@router.get("/trending", response_model=List[TrendingStudentResponse])
def trending_students(db: Session = Depends(get_db)):
    return get_trending_students(db)

@router.get("/internship")
def get_job_data(master_job_id: int | None = Query(None, description="Fetch Master Job Only"),job_id: int | None = Query(None, description="Fetch UI Success Card"),db: Session = Depends(get_db)):
    if master_job_id and job_id:
        raise HTTPException(
            status_code=400,
            detail="Provide ONLY ONE: master_job_id OR job_id"
        )
    if master_job_id is not None:
        job = fetch_master_job(db, master_job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Master Job not found")
        return job

    if job_id is not None:
        response = fetch_success_ui_by_job_id(db, job_id)
        if not response:
            raise HTTPException(status_code=404, detail="Job Opening not found")
        return response

    raise HTTPException(status_code=400, detail="Provide master_job_id OR job_id")

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


@router.delete("/{id}")
def delete_record(id: int,db: Session = Depends(get_db)):
    delete_by_id(db, id)
    return {
        "status": True,
        "message": "Deleted successfully"
    }
