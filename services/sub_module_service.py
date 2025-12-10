from sqlalchemy.orm import Session
from models.master_sub_module import MasterSubModule

def create_sub_module(db: Session, data):
    # obj = MasterSubModule(**data.dict())
    obj = MasterSubModule(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_sub_modules(db: Session):
    return db.query(MasterSubModule).all()


def get_sub_module(db: Session, sub_module_id: int):
    return db.query(MasterSubModule).filter(MasterSubModule.id == sub_module_id).first()


def update_sub_module(db: Session, sub_module_id: int, data):
    obj = get_sub_module(db, sub_module_id)
    if not obj:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_sub_module(db: Session, sub_module_id: int):
    obj = get_sub_module(db, sub_module_id)
    if not obj:
        return False

    db.delete(obj)
    db.commit()
    return True
