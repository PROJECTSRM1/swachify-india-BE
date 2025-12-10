from sqlalchemy.orm import Session
from models.home_service import HomeService

def create_home_service(db: Session, data):
    new_service = HomeService(**data.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

def get_all_home_services(db: Session):
    return db.query(HomeService).all()

def get_home_service_by_id(db: Session, service_id: int):
    return db.query(HomeService).filter(HomeService.id == service_id).first()

def delete_home_service(db: Session, service_id: int):
    service = get_home_service_by_id(db, service_id)
    if not service:
        return None
    db.delete(service)
    db.commit()
    return True
