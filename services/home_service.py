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
















# # from sqlalchemy.orm import Session
# # from models.home_service import HomeService

# # def create_home_service(db: Session, data):
# #     new_service = HomeService(**data.dict())
# #     db.add(new_service)
# #     db.commit()
# #     db.refresh(new_service)
# #     return new_service

# # def get_all_home_services(db: Session):
# #     return db.query(HomeService).all()

# # def get_home_service_by_id(db: Session, service_id: int):
# #     return db.query(HomeService).filter(HomeService.id == service_id).first()

# # def delete_home_service(db: Session, service_id: int):
# #     service = get_home_service_by_id(db, service_id)
# #     if not service:
# #         return None
# #     db.delete(service)
# #     db.commit()
# #     return True






# from sqlalchemy.orm import Session
# from fastapi import HTTPException

# from models.home_service import HomeService
# from models.master_module import MasterModule
# from models.master_sub_module import MasterSubModule
# from models.master_service import MasterService
# from models.master_sub_service import MasterSubService
# from models.master_sub_group import MasterSubGroup
# from models.master_time_slot import MasterTimeSlot

# from schemas.service_schema import HomeServiceCreate

# def create_home_service(db: Session, data: HomeServiceCreate):

#     sub_group = db.query(MasterSubGroup).filter(
#         MasterSubGroup.id == data.sub_group_id,
#         MasterSubGroup.is_active == True
#     ).first()
#     if not sub_group or not sub_group.sub_service_id:
#         raise HTTPException(400, "Invalid sub group mapping")

#     sub_service = db.query(MasterSubService).filter(
#         MasterSubService.id == sub_group.sub_service_id,
#         MasterSubService.is_active == True
#     ).first()
#     if not sub_service or not sub_service.service_id:
#         raise HTTPException(400, "Invalid sub service mapping")

#     service = db.query(MasterService).filter(
#         MasterService.id == sub_service.service_id,
#         MasterService.is_active == True
#     ).first()
#     if not service or not service.sub_module_id:
#         raise HTTPException(400, "Invalid service mapping")

#     sub_module = db.query(MasterSubModule).filter(
#         MasterSubModule.id == service.sub_module_id,
#         MasterSubModule.is_active == True
#     ).first()
#     if not sub_module or not sub_module.module_id:
#         raise HTTPException(400, "Invalid sub module mapping")

#     module = db.query(MasterModule).filter(
#         MasterModule.id == sub_module.module_id,
#         MasterModule.is_active == True
#     ).first()
#     if not module:
#         raise HTTPException(400, "Invalid module mapping")

#     home_service = HomeService(
#         module_id=module.id,
#         sub_module_id=sub_module.id,
#         service_id=service.id,
#         sub_service_id=sub_service.id,
#         sub_group_id=sub_group.id,

#         full_name=data.full_name,
#         email=data.email,
#         mobile=data.mobile,
#         address=data.address,
#         service_type_id=data.service_type_id,
#         problem_description=data.problem_description,
#         property_size_sqft=data.property_size_sqft,
#         add_on_id=data.add_on_id,
#         preferred_date=data.preferred_date,
#         time_slot_id=data.time_slot_id,
#         special_instructions=data.special_instructions,
#         payment_type_id=data.payment_type_id
#     )

#     db.add(home_service)
#     db.commit()
#     db.refresh(home_service)
#     return home_service



# def get_all_home_services(db: Session):
#     return db.query(HomeService).all()


# def get_home_service_by_id(db: Session, service_id: int):
#     service = db.query(HomeService).filter(HomeService.id == service_id).first()
#     if not service:
#         raise HTTPException(404, "Service not found")
#     return service


# def delete_home_service(db: Session, service_id: int):
#     service = get_home_service_by_id(db, service_id)
#     db.delete(service)
#     db.commit()
#     return {"message": "Service deleted successfully"}
