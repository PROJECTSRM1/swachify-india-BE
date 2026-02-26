from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi import HTTPException,status
from models.generated_models import MasterProject, MasterStatus, MasterTaskType, ProductRegistration, Tasks, UserRegistration
from schemas.swachify_products_schema import (ProductRegistrationCreate,ProductRegistrationUpdate, TaskCreate)
from fastapi import HTTPException
from models.generated_models import ProductRegistration,ProductOrder,UserRegistration,MasterVehicleType,TaskHistory,Tasks
from schemas.swachify_products_schema import (ProductRegistrationCreate,ProductRegistrationUpdate,ProductOrderCreate,TaskHistoryCreate)

def create_product_registration(db: Session, request: ProductRegistrationCreate):

    new_product = ProductRegistration(
        user_id=request.user_id,
        category_id=request.category_id,
        company_name=request.company_name,
        product_name=request.product_name,
        address=request.address,
        product_price=request.product_price,
        description=request.description,
        product_image=request.product_image,
        longitude=request.longitude,
        latitude=request.latitude,

        # ✅ Auto assign created_by = user_id
        created_by=request.user_id,

        is_active=request.is_active
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_product_registration_by_id(db: Session,product_id: int):
    product = db.query(ProductRegistration).filter(
        ProductRegistration.id == product_id,
        ProductRegistration.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

def get_all_product_registrations(db: Session):
    return db.query(ProductRegistration).filter(
        ProductRegistration.is_active == True
    ).all()

def update_product_registration(db: Session,product_id: int,payload: ProductRegistrationUpdate):
    product = get_product_registration_by_id(db, product_id)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)
    product.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product

def delete_product_registration(db: Session,product_id: int,modified_by: int):
    product = get_product_registration_by_id(db, product_id)
    product.is_active = False
    product.modified_by = modified_by
    product.modified_date = datetime.utcnow()
    db.commit()
    return {"message": "Product deleted successfully"}

#---------------------
#task service
#----------------------
def create_task(db: Session,payload: TaskCreate,created_by: int):
    if not db.query(MasterProject).filter(
        MasterProject.id == payload.project_id,
        MasterProject.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project_id"
        )

    if not db.query(MasterTaskType).filter(
        MasterTaskType.id == payload.task_type_id,
        MasterTaskType.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task_type_id"
        )

    if not db.query(MasterStatus).filter(
        MasterStatus.id == payload.status_id,
        MasterStatus.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status_id"
        )

    if not db.query(UserRegistration).filter(
        UserRegistration.id == payload.user_id,
        UserRegistration.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assignee_user_id"
        )

    task = Tasks(
        title=payload.title,
        description=payload.description,
        task_type_id=payload.task_type_id,
        
        project_id=payload.project_id,
        user_id=payload.user_id, 
        reporting_manager_id=payload.reporting_manager_id,
        task_manager_id=payload.task_manager_id,
        status_id=payload.status_id,
        due_date=payload.due_date,
        efforts_in_days=payload.efforts_in_days,
        created_by=created_by
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session,task_id: int,status_id: int,modified_by: int):

    task = db.query(Tasks).filter(
        Tasks.id == task_id,
        Tasks.is_active == True
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if not db.query(MasterStatus).filter(
        MasterStatus.id == status_id,
        MasterStatus.is_active == True
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status_id"
        )

    task.status_id = status_id
    task.modified_by = modified_by

    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int):
    task = (
        db.query(Tasks)
        .filter(
            Tasks.id == task_id,
            Tasks.is_active == True
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task



def create_product_order(db: Session, order_data: ProductOrderCreate):

    # 🔎 Validate User
    user = db.query(UserRegistration).filter(
        UserRegistration.id == order_data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )

    # 🔎 Validate Product
    product = db.query(ProductRegistration).filter(
        ProductRegistration.id == order_data.product_id,
        ProductRegistration.is_active == True
    ).first()

    if not product:
        raise HTTPException(
            status_code=400,
            detail="Invalid product_id. Product does not exist."
        )

    # 🔎 Validate Vehicle Type (if provided)
    if order_data.vehicle_type_id:
        vehicle = db.query(MasterVehicleType).filter(
            MasterVehicleType.id == order_data.vehicle_type_id
        ).first()

        if not vehicle:
            raise HTTPException(
                status_code=400,
                detail="Invalid vehicle_type_id. Vehicle type does not exist."
            )

    # ✅ Create Order
    new_order = ProductOrder(**order_data.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order




def get_product_order_by_id(db: Session, order_id: int) -> Optional[ProductOrder]:
    return db.query(ProductOrder).filter(
        ProductOrder.id == order_id,
        ProductOrder.is_active == True
    ).first()



def create_task_history(db: Session, payload: TaskHistoryCreate):

    # ✅ Validate created_by
    if payload.created_by:
        creator = db.query(UserRegistration).filter(
            UserRegistration.id == payload.created_by,
            UserRegistration.is_active == True
        ).first()

        if not creator:
            raise HTTPException(
                status_code=400,
                detail="Invalid created_by. User does not exist."
            )

    # existing validations
    task = db.query(Tasks).filter(
        Tasks.id == payload.task_id
    ).first()

    if not task:
        raise HTTPException(status_code=400, detail="Invalid task_id")

    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    new_entry = TaskHistory(**payload.model_dump())

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry




def get_task_history_by_id(db: Session, history_id: int) -> Optional[TaskHistory]:
    return db.query(TaskHistory).filter(
        TaskHistory.id == history_id,
        TaskHistory.is_active == True
    ).first()