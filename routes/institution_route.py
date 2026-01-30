from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List


from core.database import get_db
from schemas.institution_schema import (
    InstitutionRegistrationCreate,
    InstitutionRegistrationResponse,
    InstitutionBranchCreate,
    InstitutionBranchResponse,
     StudentAcademicDetailsSchema
)
from services.institution_service import (
    create_institution,
    get_all_branches,
    get_institution_by_id,
    create_institution_branch,
    get_branches_by_institution,
  get_student_full_academic_details 
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
    "/{institution_id}",
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


@router.get(
    "/students/academic-details",
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