# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from core.database import get_db
# # from services.home_service import (
# #     create_home_service,
# #     get_home_services,
# #     get_home_service_by_id,
# #     delete_home_service
# # )

# router = APIRouter(prefix="/home-service", tags=["Home Services"])


# @router.post("/")
# def create_service(payload: HomeServiceCreate, db: Session = Depends(get_db)):
#     return create_home_service(payload, db)


# @router.get("/")
# def fetch_all(db: Session = Depends(get_db)):
#     return get_home_services(db)


# @router.get("/{service_id}")
# def fetch_by_id(service_id: int, db: Session = Depends(get_db)):
#     return get_home_service_by_id(service_id, db)


# @router.delete("/{service_id}")
# def delete(service_id: int, db: Session = Depends(get_db)):
#     return delete_home_service(service_id, db)
