from sqlalchemy.orm import Session
from models.master_sub_service import MasterSubService
from schemas.master_sub_service_schema import SubServiceCreate, SubServiceUpdate

def build_response(record: MasterSubService):
    return {
        "id": record.id,
        "sub_service_name": record.sub_service_name,
        "is_active": record.is_active,

        "service_id": record.service_id,
        "service_name": record.service.service_name,

        "sub_module_id": record.service.sub_module_id,
        "sub_module_name": record.service.submodule.sub_module_name,

        "module_id": record.service.submodule.module_id,
        "module_name": record.service.submodule.module.module_name,
    }

def create_sub_service(db: Session, data: SubServiceCreate):
    record = MasterSubService(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return build_response(record)

def get_all_sub_services(db: Session):
    return [build_response(r) for r in db.query(MasterSubService).all()]

def get_sub_service(db: Session, id: int):
    r = db.query(MasterSubService).filter(MasterSubService.id == id).first()
    if not r:
        return None
    return build_response(r)

def update_sub_service(db: Session, id: int, data: SubServiceUpdate):
    r = db.query(MasterSubService).filter(MasterSubService.id == id).first()
    if not r:
        return None
    for k, v in data.dict().items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return build_response(r)

def delete_sub_service(db: Session, id: int):
    r = db.query(MasterSubService).filter(MasterSubService.id == id).first()
    if not r:
        return None
    db.delete(r)
    db.commit()
    return True
