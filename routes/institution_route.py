from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.institution_schema import (
    ExamScheduleCreate,
    ExamScheduleListResponse,
    InstitutionRegistrationCreate,
    InstitutionRegistrationResponse,
    InstitutionBranchCreate,
    InstitutionBranchResponse
)
from services.institution_service import (
    create_exam_schedule,
    create_institution,
    fetch_exam_schedule,
    fetch_students_by_branch,
    get_all_branches,
    get_institution_by_id,
    create_institution_branch,
    get_branches_by_institution
)


router = APIRouter(
    prefix="/institution",
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


# ✅ GET ALL branches (STATIC)
@router.get("/all/branches")
def get_all_branches_api(db: Session = Depends(get_db)):
    return get_all_branches(db)

# get by id 
@router.get("/institutions/{institution_id}/branches",
    response_model=list[InstitutionBranchResponse]
)
def get_branches_by_institution_api(
    institution_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_branches_by_institution(db, institution_id)

# # ✅ GET ALL branches (STATIC)
# @router.get(
#     "/branches",
#     response_model=list[InstitutionBranchResponse]
# )
# def get_all_branches_api(
#     db: Session = Depends(get_db)
# ):
#     return get_all_branches(db)




# get_students_by_branch route 

@router.get("/students/by_branch_id")
def get_students_by_branch(
    branch_id: int,
    db: Session = Depends(get_db)
):
     return fetch_students_by_branch(db, branch_id)

#ExamSchedule route 

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