from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.institution_schema import (
    InstitutionRegistrationCreate,
    InstitutionRegistrationResponse,
    InstitutionBranchCreate,
    InstitutionBranchResponse,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse
)

from services.institution_service import (
    create_institution,
    get_institution_by_id,
    create_institution_branch,
    get_all_branches,
    get_branches_by_institution,
    create_student_profile,
    get_all_students,
    get_student_by_id,
    update_student_profile,
    delete_student_profile,
    get_active_branch_directory,
    fetch_students_by_branch
)

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


@router.get("/branch-directory")
def preview_branch_directory(
    branch_id: int = Query(
        -1,
        description="Pass branch_id or -1 to fetch all active branches"
    ),
    db: Session = Depends(get_db)
):
    return get_active_branch_directory(db, branch_id)


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


@router.get(
    "/student/{student_id}",
    response_model=StudentProfileResponse
)
def get_student_api(
    student_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    return get_student_by_id(db, student_id)


@router.get("/students/by-branch")
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
