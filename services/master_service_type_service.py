from sqlalchemy.orm import Session
from models.master_service_type import MasterServiceType
from schemas.master_service_type_schema import ServiceTypeCreate, ServiceTypeUpdate

def create_service_type(db: Session, data: ServiceTypeCreate):
    record = MasterServiceType(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_service_types(db: Session):
    return db.query(MasterServiceType).all()

def get_service_type(db: Session, id: int):
    return db.query(MasterServiceType).filter(MasterServiceType.id == id).first()

def update_service_type(db: Session, id: int, data: ServiceTypeUpdate):
    record = get_service_type(db, id)
    if not record:
        return None
    for key, value in data.dict().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

def delete_service_type(db: Session, id: int):
    record = get_service_type(db, id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return True
