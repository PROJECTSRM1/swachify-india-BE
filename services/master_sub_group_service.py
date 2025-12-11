from sqlalchemy.orm import Session
from models.master_sub_group import MasterSubGroup
from schemas.master_sub_group_schema import SubGroupCreate, SubGroupUpdate

def build_response(record: MasterSubGroup):
    ss = record.sub_service
    srv = ss.service
    sm = srv.submodule
    module = sm.module

    return {
        "id": record.id,
        "sub_group_name": record.sub_group_name,
        "is_active": record.is_active,

        # direct fk
        "sub_service_id": record.sub_service_id,
        "sub_service_name": ss.sub_service_name,

        # from service table
        "service_id": srv.id,
        "service_name": srv.service_name,

        # from sub module
        "sub_module_id": sm.id,
        "sub_module_name": sm.sub_module_name,

        # from module
        "module_id": module.id,
        "module_name": module.module_name,
    }


def create_sub_group(db: Session, data: SubGroupCreate):
    record = MasterSubGroup(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return build_response(record)


def get_all_sub_groups(db: Session):
    records = db.query(MasterSubGroup).all()
    return [build_response(r) for r in records]


def get_sub_group(db: Session, id: int):
    r = db.query(MasterSubGroup).filter(MasterSubGroup.id == id).first()
    if not r:
        return None
    return build_response(r)


def update_sub_group(db: Session, id: int, data: SubGroupUpdate):
    r = db.query(MasterSubGroup).filter(MasterSubGroup.id == id).first()
    if not r:
        return None
    for k, v in data.dict().items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return build_response(r)


def delete_sub_group(db: Session, id: int):
    r = db.query(MasterSubGroup).filter(MasterSubGroup.id == id).first()
    if not r:
        return None
    db.delete(r)
    db.commit()
    return True
