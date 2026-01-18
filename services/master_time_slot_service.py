from sqlalchemy.orm import Session
# from models.master_time_slot import MasterTimeSlot
from models.generated_models import MasterTimeSlot
from schemas.master_time_slot_schema import TimeSlotCreate, TimeSlotUpdate

def build_timeslot_response(record: MasterTimeSlot):
    home_services = record.home_services

    return {
        "id": record.id,
        "time_slot": record.time_slot,
        "is_active": record.is_active,
        "home_service_count": len(home_services),
        "home_services": home_services
    }

def create_time_slot(db: Session, data: TimeSlotCreate):
    record = MasterTimeSlot(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return build_timeslot_response(record)

def get_all_time_slots(db: Session):
    records = db.query(MasterTimeSlot).all()
    return [build_timeslot_response(r) for r in records]

def get_time_slot(db: Session, id: int):
    record = db.query(MasterTimeSlot).filter(MasterTimeSlot.id == id).first()
    if not record:
        return None
    return build_timeslot_response(record)

def update_time_slot(db: Session, id: int, data: TimeSlotUpdate):
    record = db.query(MasterTimeSlot).filter(MasterTimeSlot.id == id).first()
    if not record:
        return None

    for k, v in data.dict().items():
        setattr(record, k, v)

    db.commit()
    db.refresh(record)
    return build_timeslot_response(record)

def delete_time_slot(db: Session, id: int):
    record = db.query(MasterTimeSlot).filter(MasterTimeSlot.id == id).first()
    if not record:
        return None
    db.delete(record)
    db.commit()
    return True
