from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from core.database import get_db
from core.dependencies import get_current_user
from models.generated_models import UserRegistration,JobApplication
from schemas.student_education_schema import (
    JobOpeningCreate,
    JobOpeningResponse,
    JobApplicationCreate,
    JobApplicationResponse
)
from services.student_education_service import (
    create_job_openings,
    get_active_job_openings,
    get_job_openings,
    get_job_opening,
    apply_job_service,
    delete_job_opening_service
)

# Router
router = APIRouter( prefix="/api/jobs",tags=["Jobs Module"])

bearer_scheme = HTTPBearer()

# job openings
@router.post("/openings", response_model=JobOpeningResponse)
def create_opening(payload: JobOpeningCreate,db: Session = Depends(get_db),current_user: UserRegistration = Depends(get_current_user)):
    return create_job_openings(
        db=db,
        data=payload,            
        user_id=current_user.id
    )
@router.get("/openings",response_model=list[JobOpeningResponse])
def list_openings(db: Session = Depends(get_db)):
    return get_job_openings(db)

@router.get("/openings/{job_id}",response_model=JobOpeningResponse)
def get_opening(job_id: int,db: Session = Depends(get_db)):
    job = get_job_opening(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job opening not found")
    return job
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

@router.get("/active")
def get_all_active_jobs(
    category_id: int = Query(-1, description="Pass category_id to filter, -1 for all"),
    db: Session = Depends(get_db)
):
    return get_active_job_openings(db, category_id)


@router.delete("/openings/{opening_id}")
def delete_job_opening(opening_id: int,db: Session = Depends(get_db),current_user: UserRegistration = Depends(get_current_user)):
    return delete_job_opening_service(
        db=db,
        opening_id=opening_id,
        user_id=current_user.id
    )



#JOB APPLICATIONS

@router.post("/apply",response_model=JobApplicationResponse)
def apply_job(payload: JobApplicationCreate,db: Session = Depends(get_db),current_user: UserRegistration = Depends(get_current_user)):
    return apply_job_service(
        db=db,
        payload=payload,
        user_id=current_user.id
    )


@router.get("/jobs/applications",response_model=list[JobApplicationResponse])
def get_my_job_applications(db: Session = Depends(get_db),current_user: UserRegistration = Depends(get_current_user)):
    return (
        db.query(JobApplication)
        .filter(
            JobApplication.user_id == current_user.id,
            JobApplication.is_active == True
        )
        .order_by(JobApplication.created_date.desc())
        .all()
    )