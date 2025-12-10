from sqlalchemy.orm import Session
from models.master_module import MasterModule
from schemas.master_module_schema import MasterModuleCreate, MasterModuleUpdate

def create_module(db: Session, data: MasterModuleCreate):
    # new_module = MasterModule(**data.dict())
    new_module = MasterModule(**data)
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


def get_all_modules(db: Session):
    return db.query(MasterModule).all()


def get_module_by_id(db: Session, module_id: int):
    return db.query(MasterModule).filter(MasterModule.id == module_id).first()


def update_module(db: Session, module_id: int, data: MasterModuleUpdate):
    module = get_module_by_id(db, module_id)
    if not module:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(module, key, value)

    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: int):
    module = get_module_by_id(db, module_id)
    if not module:
        return False

    db.delete(module)
    db.commit()
    return True
