from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.institution_schema import (
    InstitutionRegistrationCreate,
    InstitutionRegistrationResponse,
    InstitutionBranchCreate,
    InstitutionBranchResponse
)
from services.institution_service import (
    create_institution,
    get_all_branches,
    get_institution_by_id,
    create_institution_branch,
    get_branches_by_institution
)

from schemas.institution_schema import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse
)
from services.institution_service import (
    create_student_profile,
    get_all_students,
    get_student_by_id,
    update_student_profile,
    delete_student_profile
)
from services.institution_service import get_active_branch_directory


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


@router.post(
    "/",
    response_model=StudentProfileResponse
)
def create_student(
    payload: StudentProfileCreate,
    db: Session = Depends(get_db)
):
    return create_student_profile(db, payload)


@router.get(
    "/",
    response_model=list[StudentProfileResponse]
)
def get_students(db: Session = Depends(get_db)):
    return get_all_students(db)

@router.get("/branch-directory")
def preview_branch_directory(
    branch_id: int = Query(
        -1,
        description="Pass branch_id or -1 to fetch all active branches"
    ),
    db: Session = Depends(get_db)
):
    return get_active_branch_directory(db, branch_id)

@router.get(
    "/{student_id}",
    response_model=StudentProfileResponse
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_by_id(db, student_id)


@router.put(
    "/{student_id}",
    response_model=StudentProfileResponse
)
def update_student(
    student_id: int,
    payload: StudentProfileUpdate,
    db: Session = Depends(get_db)
):
    return update_student_profile(db, student_id, payload)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return delete_student_profile(db, student_id)

