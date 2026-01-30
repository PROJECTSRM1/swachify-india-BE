from sqlalchemy.orm import Session
from models.generated_models import StudentProfile
from schemas.student_profile_schema import (
    StudentProfileCreate,
    StudentProfileUpdate
)
from fastapi import HTTPException, status
from datetime import datetime


def create_student_profile(db: Session, payload: StudentProfileCreate):
    existing = db.query(StudentProfile).filter(
        StudentProfile.student_id == payload.student_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
