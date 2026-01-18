from sqlalchemy.orm import Session

from models.generated_models import MasterModule,MasterSubModule,MasterService,MasterSubService,MasterSubGroup,MasterServiceType

def get_master_data(db: Session):
    return {
    "modules": db.query(MasterModule).all(),
    "sub_modules": db.query(MasterSubModule).all(),
    "services": db.query(MasterService).all(),
    "sub_services": db.query(MasterSubService).all(),
    "sub_groups": db.query(MasterSubGroup).all(),
    "service_types": db.query(MasterServiceType).all(),
    }