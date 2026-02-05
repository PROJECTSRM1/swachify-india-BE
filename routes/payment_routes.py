from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import razorpay
import os

from core.database import get_db          
from models.generated_models import HomeServiceBooking

router = APIRouter(prefix="/api/payment", tags=["Payment"])

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
    """
    Create a Razorpay order.
    
    REQUEST BODY:
    {
        "amount": 50000,  // Amount in paisa (50000 = ₹500)
        "bookingId": 129
    }
    
    RESPONSE:
    {
        "id": "order_xxxxx",
        "entity": "order",
        "amount": 50000,
        "amount_paid": 0,
        "currency": "INR",
        "receipt": "receipt_129",
        ...
    }
    """
    try:
        order = client.order.create({
            "amount": req.amount,
            "currency": "INR",
            "receipt": f"receipt_{req.bookingId}",
        })
        return order
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create order: {str(e)}"
        )


@router.post("/verify-payment")
def verify_payment(
    req: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": req.order_id,
            "razorpay_payment_id": req.payment_id,
            "razorpay_signature": req.signature,
        })

       
        booking = db.get(HomeServiceBooking, req.home_service_id)
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
