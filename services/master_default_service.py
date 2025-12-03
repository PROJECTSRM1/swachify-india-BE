from sqlalchemy.orm import Session
from models.master.master_skill import MasterSkill
from models.master.master_state import MasterState
from models.master.master_district import MasterDistrict
from models.master.master_gender import MasterGender

def fetch_default_skill(db: Session):
    return db.query(MasterSkill).filter(MasterSkill.is_active == True).first()

def fetch_default_state(db: Session):
    return db.query(MasterState).filter(MasterState.is_active == True).first()

def fetch_default_district(db: Session, state_id: int):
    return db.query(MasterDistrict).filter(
        MasterDistrict.state_id == state_id,
        MasterDistrict.is_active == True
    ).first()

def fetch_default_gender(db: Session):
    """
    Returns the first active gender from master_gender table.
    """
    return db.query(MasterGender).filter(
        MasterGender.is_active == True
    ).order_by(MasterGender.id.asc()).first()
