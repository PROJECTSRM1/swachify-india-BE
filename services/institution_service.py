from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from models.generated_models import (
    InstitutionRegistration,
    InstitutionBranch
)
from schemas.institution_schema import (
    InstitutionRegistrationCreate,
    InstitutionBranchCreate
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

# get_students_by_branch service

def fetch_students_by_branch(db, branch_id: int):
    query = text("""
        SELECT * FROM fn_get_students_by_branch(:branch_id)
    """)
    result = db.execute(query, {"branch_id": branch_id})
    return result.mappings().all()   

#ExamSchedule service

def create_exam_schedule(db, data):
    query = text("""
        INSERT INTO exam_schedule (
            branch_id,
            exam_type,
            subject_name,
            exam_date,
            created_by,
            is_active
        )
        VALUES (
            :branch_id,
            :exam_type,
            :subject_name,
            :exam_date,
            :created_by,
            true
        )
        RETURNING id
    """)

    result = db.execute(query, {
        "branch_id": data.branch_id,
        "exam_type": data.exam_type,
        "subject_name": data.subject_name,
        "exam_date": data.exam_date,
        "created_by": data.created_by
    })

    db.commit()
    return result.fetchone()[0]

#ExamList Service

def fetch_exam_schedule(db, branch_id: int, exam_type: str):
    query = text("""
        SELECT * FROM fn_get_exam_schedule(:branch_id, :exam_type)
    """)

    result = db.execute(query, {
        "branch_id": branch_id,
        "exam_type": exam_type
    })

    return result.mappings().all()  