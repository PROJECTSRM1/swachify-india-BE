from sqlalchemy.orm import Session
from models.master_service import MasterService

def get_all_services(db:Session):
    return db.query(MasterService).all()

def get_service(db:Session,service_id:int):
    return db.query(MasterService).filter(MasterService.id == service_id).first()

def create_service(db:Session,data):
    # service = MasterService(**data.dict())
    service = MasterService(**data)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def update_service(db:Session,service_id:int,data):
    service = get_service(db,service_id)
    if not service:
        return None
    for key,value in data.dict(exclude_unset=True).items():
        setattr(service,key,value)

    db.commit()
    db.refresh(service)
    return service

def delete_service(db:Session,service_id:int):
    service = get_service(db,service_id)
    if not service:
        return None
    db.delete(service)
    db.commit()
    return service