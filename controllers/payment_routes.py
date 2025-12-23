from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import razorpay
import os

from core.database import get_db          
from models.home_service import HomeService 

router = APIRouter()

# Razorpay client
client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET"),
    )
)




class CreateOrderRequest(BaseModel):
    amount: int
    bookingId: int


class VerifyPaymentRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str
    home_service_id: int  




@router.post("/create-order")
def create_order(req: CreateOrderRequest):
    order = client.order.create({
        "amount": req.amount,
        "currency": "INR",
        "receipt": f"receipt_{req.bookingId}",
    })
    return order


@router.post("/verify-payment")
def verify_payment(
    req: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1️⃣ Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": req.order_id,
            "razorpay_payment_id": req.payment_id,
            "razorpay_signature": req.signature,
        })

       
        booking = db.get(HomeService, req.home_service_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

     
        booking.payment_done = True
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "Payment verified & booking updated",
            "booking_id": booking.id,
            "payment_done": booking.payment_done,
        }

    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay signature"
        )
