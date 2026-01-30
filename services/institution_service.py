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
