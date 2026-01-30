from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException,status

from models.generated_models import (
    InstitutionRegistration,
    InstitutionBranch,
    StudentProfile
)
from sqlalchemy import text
from typing import List
from schemas.institution_schema import (
    InstitutionRegistrationCreate,
    InstitutionBranchCreate,
    StudentAcademicDetailsSchema,
    StudentProfileCreate,
    StudentProfileUpdate
)



# ======================================================
# INSTITUTION REGISTRATION SERVICES
# ======================================================

def create_institution(
    db: Session,
    payload: InstitutionRegistrationCreate
):
    institution = InstitutionRegistration(
        **payload.dict(),
        created_date=datetime.utcnow()
    )
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return institution

def get_all_branches(db: Session):
    return db.query(InstitutionBranch).all()

def get_institution_by_id(
    db: Session,
    institution_id: int
):
    institution = db.query(InstitutionRegistration).filter(
        InstitutionRegistration.id == institution_id,
        InstitutionRegistration.is_active == True
    ).first()

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    return institution


# def get_all_branches(db: Session):
#     return db.query(InstitutionBranch).all()


# ======================================================
# INSTITUTION BRANCH SERVICES
# ======================================================

def create_institution_branch(
    db: Session,
    payload: InstitutionBranchCreate
):
    branch = InstitutionBranch(
        **payload.dict(),
        created_date=datetime.utcnow()
    )
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


def get_branches_by_institution(
    db: Session,
    institution_id: int
):
    return db.query(InstitutionBranch).filter(
        InstitutionBranch.institution_id == institution_id,
        InstitutionBranch.is_active == True
    ).all()

# ======================================================
# STUDENT ACADEMIC DETAILS
# ======================================================

def get_student_full_academic_details(
    db: Session,
    student_id: str = "-1",
    institution_id: int = -1
) -> List[StudentAcademicDetailsSchema]:
    """
    Fetch full student academic details using DB function
    fn_get_student_full_details
    """

    query = text("""
        SELECT *
        FROM fn_get_student_full_details(:student_id, :institution_id)
    """)

    result = db.execute(
        query,
        {
            "student_id": student_id,
            "institution_id": institution_id
        }
    )

    rows = result.mappings().all()

    return [StudentAcademicDetailsSchema(**row) for row in rows]


def create_student_profile(db: Session, payload: StudentProfileCreate):
    existing = db.query(StudentProfile).filter(
        StudentProfile.student_id == payload.student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # type: ignore
            detail="Student profile already exists"
        )

    student = StudentProfile(**payload.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_all_students(db: Session):
    return db.query(StudentProfile).filter(
        StudentProfile.is_active == True
    ).all()


def get_active_branch_directory(db: Session, branch_id: int):
    query = text(
        "SELECT * FROM fn_get_branch_directory(:branch_id)"
    )
    result = db.execute(query, {"branch_id": branch_id})
    return result.mappings().all()

def get_student_by_id(db: Session, student_id: int):
    student = db.query(StudentProfile).filter(
        StudentProfile.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


def update_student_profile(
    db: Session,
    student_id: int,
    payload: StudentProfileUpdate
):
    student = get_student_by_id(db, student_id)

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(student, key, value)

    student.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(student)
    return student


def delete_student_profile(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    student.is_active = False
    student.modified_date = datetime.utcnow()
    db.commit()
    return {"message": "Student profile deactivated successfully"}


# get_students_by_branch service

def fetch_students_by_branch(db, branch_id: int):
    query = text("""
        SELECT * FROM fn_get_students_by_branch(:branch_id)
    """)
    result = db.execute(query, {"branch_id": branch_id})
    return result.mappings().all()   
