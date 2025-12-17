from sqlalchemy.orm import Session

from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from models.master_service import MasterService
from models.master_sub_service import MasterSubService
from models.master_sub_group import MasterSubGroup
from models.master_service_type import MasterServiceType


def get_master_data(db: Session):
    return {
        "modules": db.query(MasterModule).all(),
        "sub_modules": db.query(MasterSubModule).all(),
        "services": db.query(MasterService).all(),
        "sub_services": db.query(MasterSubService).all(),
        "sub_groups": db.query(MasterSubGroup).all(),
        "service_types": db.query(MasterServiceType).all(),
    }
