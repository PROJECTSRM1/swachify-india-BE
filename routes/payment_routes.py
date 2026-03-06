from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import razorpay
import os
from dotenv import load_dotenv
from core.database import get_db
from models.generated_models import HomeServiceBooking

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api/payment", tags=["Payment"])

# Validate Razorpay Keys
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise Exception("Razorpay keys not found in environment variables")

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# -------------------------
# REQUEST MODELS
# -------------------------

class CreateOrderRequest(BaseModel):
    amount: int
    bookingId: int


class VerifyPaymentRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str
    home_service_id: int


# -------------------------
# CREATE ORDER API
# -------------------------

@router.post("/create-order")
def create_order(req: CreateOrderRequest):
    """
    Create a Razorpay Order
    amount must be in paisa
    """

    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    try:
        order = client.order.create({
            "amount": req.amount,
            "currency": "INR",
            "receipt": f"receipt_{req.bookingId}",
            "payment_capture": 1
        })

        return {
            "status": "success",
            "order": order
        }

    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")

    except razorpay.errors.ServerError as e:
        raise HTTPException(status_code=500, detail=f"Razorpay Server Error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")


# -------------------------
# VERIFY PAYMENT API
# -------------------------

@router.post("/verify-payment")
def verify_payment(
    req: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    try:
        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": req.order_id,
            "razorpay_payment_id": req.payment_id,
            "razorpay_signature": req.signature,
        })

        # Fetch booking
        booking = db.get(HomeServiceBooking, req.home_service_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Update payment status
        booking.payment_done = True
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "Payment verified successfully",
            "booking_id": booking.id,
            "payment_done": booking.payment_done,
        }

    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Razorpay signature")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")