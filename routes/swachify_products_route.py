from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.swachify_products_schema import (
    ProductOrderCreate,
    ProductOrderResponse,
    ProductRegistrationCreate,
    # ProductRegistrationUpdate,
    ProductRegistrationResponse,
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    ProductOrderCreate,
    ProductOrderResponse,
    TaskHistoryCreate,
    TaskHistoryResponse

)
from services.swachify_products_service import (
    create_product_registration,
    get_product_registration_by_id,
    get_all_product_registrations,
    update_task_status,
    create_task,
    get_task_by_id,
    update_task_status,
    create_task_history,
    get_task_history_by_id,

    # update_product_registration,
    # delete_product_registration,
    create_product_order,
    get_product_order_by_id
)

router = APIRouter(prefix="/product-registration",tags=["Swachify Products"])

@router.post("/",response_model=ProductRegistrationResponse)
def create_product(payload: ProductRegistrationCreate,db: Session = Depends(get_db)):
    return create_product_registration(db, payload)

@router.get("/{product_id}",response_model=ProductRegistrationResponse)
def get_product(product_id: int,db: Session = Depends(get_db)):
    return get_product_registration_by_id(db, product_id)

@router.get("/",response_model=List[ProductRegistrationResponse])
def get_products(db: Session = Depends(get_db)):
    return get_all_product_registrations(db)

# @router.put("/{product_id}",response_model=ProductRegistrationResponse)
# def update_product(product_id: int,payload: ProductRegistrationUpdate,db: Session = Depends(get_db)):
#     return update_product_registration(db, product_id, payload)


# @router.delete("/{product_id}")
# def delete_product(
#     product_id: int,
#     modified_by: int,
#     db: Session = Depends(get_db)
# ):
#     return delete_product_registration(db, product_id, modified_by)

@router.post("/task",response_model=TaskResponse,summary="Create Task")
def create_task_api(payload: TaskCreate,user_id: int = Query(..., description="Logged-in user ID"),db: Session = Depends(get_db)):
    return create_task(db=db, payload=payload, created_by=user_id)

@router.put("/{task_id}/status",response_model=TaskResponse,summary="Update Task Status")
def update_task_status_api(task_id: int,payload: TaskStatusUpdate,user_id: int = Query(..., description="Logged-in user ID"),db: Session = Depends(get_db)):
    return update_task_status(
        db=db,
        task_id=task_id,
        status_id=payload.status_id,
        modified_by=user_id
    )

@router.get("/task/{task_id}", response_model=TaskResponse, summary="Get Task By ID")
def get_task_by_id_api(task_id: int, db: Session = Depends(get_db)):
    return get_task_by_id(db=db, task_id=task_id)
# ===============================
# POST - CREATE ORDER
# ===============================

@router.post("/orders", response_model=ProductOrderResponse)
def create_order(order: ProductOrderCreate, db: Session = Depends(get_db)):
    return create_product_order(db, order)


# ===============================
# GET - ORDER BY ID
# ===============================

@router.get("/orders/{order_id}", response_model=ProductOrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_product_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Product order not found")
    return order



@router.post("/task-history", response_model=TaskHistoryResponse)
def create_history(payload: TaskHistoryCreate, db: Session = Depends(get_db)):
    return create_task_history(db, payload)




@router.get("/task-history/{history_id}", response_model=TaskHistoryResponse)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history = get_task_history_by_id(db, history_id)

    if not history:
        raise HTTPException(status_code=404, detail="Task history not found")

    return history