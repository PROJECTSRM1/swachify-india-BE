from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.generated_models import (
    StudentAttendance,
    UserRegistration
)


def upsert_student_attendance(
    db: Session,
    user_id: int,
    attendance_percentage
) -> StudentAttendance:

    student = (
        db.query(UserRegistration)
        .filter(
            UserRegistration.id == user_id,
            UserRegistration.is_active == True
        )
        .first()
    )

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    record = (
        db.query(StudentAttendance)
        .filter(
            StudentAttendance.user_id == user_id,
            StudentAttendance.is_active == True
        )
        .first()
    )

    if record:
        record.attendance_percentage = attendance_percentage
    else:
        record = StudentAttendance(
            user_id=user_id,
            attendance_percentage=attendance_percentage,
            is_active=True
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record
