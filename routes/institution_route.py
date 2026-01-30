from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import random
from models.generated_models import InstitutionRegistration

from core.database import get_db

from schemas.institution_schema import (
    ExamScheduleCreate,
    ExamScheduleListResponse,
    InstitutionRegistrationCreate,
    InstitutionRegistrationResponse,
    InstitutionBranchCreate,
    InstitutionBranchResponse,
    StudentAcademicDetailsSchema,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse
)

from services.institution_service import (
    create_exam_schedule,
    create_institution,
    fetch_exam_schedule,
    get_institution_by_id,
    create_institution_branch,
    get_branches_by_institution,
    get_student_full_academic_details,
    get_all_branches,
    get_branches_by_institution,
    create_student_profile,
    get_all_students,
    get_student_by_id,
    update_student_profile,
    delete_student_profile,
    get_active_branch_directory,
    fetch_students_by_branch,
    get_management_overview
)

from pydantic import BaseModel, model_validator
from fastapi import HTTPException
from models.generated_models import InstitutionRegistration

class InstitutionLoginRequest(BaseModel):
    email_or_phone: str
    password: str

    @model_validator(mode="after")
    def check_email_or_phone(self):
        if not self.email and not self.phone_number:
            raise ValueError('Either email or phone_number must be provided')
        return self

router = APIRouter(
    prefix="/institution/student",
    tags=["Institution"]
)

# ======================================================
# INSTITUTION REGISTRATION
# ======================================================

@router.post(
    "/register",
    response_model=InstitutionRegistrationResponse
)
def register_institution_api(
    payload: InstitutionRegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_institution(db, payload)

@router.post("/login")
def institution_login(payload: InstitutionLoginRequest, db: Session = Depends(get_db)):
    user = None
    if payload.email:
        user = db.query(InstitutionRegistration).filter(
            InstitutionRegistration.is_active == True,
            InstitutionRegistration.email == payload.email
        ).first()
    elif payload.phone_number:
        user = db.query(InstitutionRegistration).filter(
            InstitutionRegistration.is_active == True,
            InstitutionRegistration.phone_number == payload.phone_number
        ).first()
    if not user or not user.password_hash == payload.password:  
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "Login successful", "institution_id": user.id}

@router.get(
    "/institution/{institution_id}",
    response_model=InstitutionRegistrationResponse
)
def get_institution_api(
    institution_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_institution_by_id(db, institution_id)


# ======================================================
# INSTITUTION BRANCH
# ======================================================

@router.post(
    "/branch",
    response_model=InstitutionBranchResponse
)
def create_branch_api(
    payload: InstitutionBranchCreate,
    db: Session = Depends(get_db)
):
    return create_institution_branch(db, payload)



@router.get("/all/branches")
def get_all_branches_api(
    db: Session = Depends(get_db)
):
    return get_all_branches(db)


@router.get(
    "/institution/{institution_id}/branches",
    response_model=list[InstitutionBranchResponse]
)
def get_branches_by_institution_api(
    institution_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_branches_by_institution(db, institution_id)



@router.get(
    "/academic-details",
    response_model=List[StudentAcademicDetailsSchema]
)
def fetch_student_full_academic_details(
    student_id: str = "-1",
    institution_id: int = -1,
    db: Session = Depends(get_db)
):
    """
    Get full student academic details.
    - student_id = -1 → all students
    - institution_id = -1 → all institutions
    """
    return get_student_full_academic_details(
        db=db,
        student_id=student_id,
        institution_id=institution_id
    )


# get_students_by_branch route 

@router.get("/by_branch_id")
def get_students_by_branch(
    branch_id: int,
    db: Session = Depends(get_db)
):
     return fetch_students_by_branch(db, branch_id)
@router.get("/branch-directory")
def preview_branch_directory(
    branch_id: int = Query(
        -1,
        description="Pass branch_id or -1 to fetch all active branches"
    ),
    db: Session = Depends(get_db)
):
    return get_active_branch_directory(db, branch_id)

@router.get("/management-overview")
def management_overview_api(
    institution_id: int = Query(
        -1,
        description="Pass institution_id or -1 for all institutions"
    ),
    academic_year: str = Query(
        "-1",
        description="Pass academic year (e.g. 2023-2024) or -1 for all"
    ),
    db: Session = Depends(get_db)
):
    return get_management_overview(
        db,
        institution_id,
        academic_year
    )

# ======================================================
# STUDENT PROFILE
# ======================================================

@router.post(
    "/student",
    response_model=StudentProfileResponse
)
def create_student_api(
    payload: StudentProfileCreate,
    db: Session = Depends(get_db)
):
    return create_student_profile(db, payload)


@router.get(
    "/students",
    response_model=list[StudentProfileResponse]
)
def get_students_api(
    db: Session = Depends(get_db)
):
    return get_all_students(db)




@router.get("/by-branch")
def get_students_by_branch_api(
    branch_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    return fetch_students_by_branch(db, branch_id)


# @router.put(
#     "/student/{student_id}",
#     response_model=StudentProfileResponse
# )
# def update_student_api(
#     student_id: int = Path(..., gt=0),
#     payload: StudentProfileUpdate = Depends(),
#     db: Session = Depends(get_db)
# ):
#     return update_student_profile(db, student_id, payload)


# @router.delete("/student/{student_id}")
# def delete_student_api(
#     student_id: int = Path(..., gt=0),
#     db: Session = Depends(get_db)
# ):
#     return delete_student_profile(db, student_id)

@router.post("/exam-schedule")
def create_exam(
    payload: ExamScheduleCreate,
    db: Session = Depends(get_db)
):
    exam_id = create_exam_schedule(db, payload)
    return {
        "message": "Exam schedule created successfully",
        "exam_schedule_id": exam_id
    }

#ExamList

@router.get(
    "/exam-schedule",
    response_model=List[ExamScheduleListResponse]
)
def get_exam_schedule(
    branch_id: int = -1,
    exam_type: str = "-1",
    db: Session = Depends(get_db)
):
    return fetch_exam_schedule(db, branch_id, exam_type)

#student profile

@router.get(
    "/{student_id}",
    response_model=StudentProfileResponse
)
def get_student_api(
    student_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_student_by_id(db, student_id)