from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.generated_models import (
    MasterInternshipStatus,
    UserRegistration
)


def upsert_student_internship(
    db: Session,
    user_id: int,
    internship_status: str
) -> MasterInternshipStatus:
    # Validate student
    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == user_id,
            UserRegistration.is_active == True
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check existing internship status
    record = (
        db.query(MasterInternshipStatus)
        .filter(
            MasterInternshipStatus.user_id == user_id,
            MasterInternshipStatus.is_active == True
        )
        .first()
    )

    if record:
        record.internship_status = internship_status
    else:
        record = MasterInternshipStatus(
            user_id=user_id,
            internship_status=internship_status,
            is_active=True
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record
