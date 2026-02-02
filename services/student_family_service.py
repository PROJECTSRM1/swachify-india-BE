from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.generated_models import (
    StudentFamilyMembers,
    UserRegistration,
    MasterRelation,
)

from schemas.student_family_schema import (
    StudentFamilyMemberCreate,
    StudentFamilyMemberUpdate,
)


def add_family_member_service(db: Session,student_id: int,payload: StudentFamilyMemberCreate,created_by: int | None = None):
    student = (
        db.query(UserRegistration)
        .filter(UserRegistration.id == student_id, UserRegistration.is_active == True)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    relation = (
        db.query(MasterRelation)
        .filter(
            MasterRelation.id == payload.relation_type_id,
            MasterRelation.is_active == True
        )
        .first()
    )
    if not relation:
        raise HTTPException(status_code=404, detail="Invalid relation type")

    record = StudentFamilyMembers(
        user_id=student_id,
        relation_type_id=payload.relation_type_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        created_by=created_by or student_id,
        is_active=True,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def update_family_member_service(db: Session,member_id: int,payload: StudentFamilyMemberUpdate,modified_by: int | None = None):
    record = (
        db.query(StudentFamilyMembers)
        .filter(
            StudentFamilyMembers.id == member_id,
            StudentFamilyMembers.is_active == True
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Family member not found")

    if payload.relation_type_id:
        relation = (
            db.query(MasterRelation)
            .filter(
                MasterRelation.id == payload.relation_type_id,
                MasterRelation.is_active == True
            )
            .first()
        )
        if not relation:
            raise HTTPException(status_code=404, detail="Invalid relation type")

        record.relation_type_id = payload.relation_type_id

    if payload.first_name is not None:
        record.first_name = payload.first_name
    if payload.last_name is not None:
        record.last_name = payload.last_name
    if payload.phone_number is not None:
        record.phone_number = payload.phone_number

    record.modified_by = modified_by
    db.commit()
    db.refresh(record)

    return record

def hard_delete_family_member_service(db: Session,member_id: int,):
    member = (
        db.query(StudentFamilyMembers)
        .filter(StudentFamilyMembers.id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Family member permanently deleted",
        "member_id": member_id
    }

def list_family_members_service(db: Session,student_id: int):
    return (
        db.query(StudentFamilyMembers)
        .filter(
            StudentFamilyMembers.user_id == student_id,
            StudentFamilyMembers.is_active == True
        )
        .all()
    )
