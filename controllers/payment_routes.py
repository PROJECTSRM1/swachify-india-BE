from fastapi import APIRouter
from pydantic import BaseModel
import razorpay
from dotenv import load_dotenv
import os


load_dotenv()

router = APIRouter()


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
class CreateOrderRequest(BaseModel):
    amount: int
    bookingId: str

@router.post("/create-order")

def create_order(req: CreateOrderRequest):
    order = client.order.create({
        "amount": req.amount,
        "currency": "INR",
        "receipt": f"receipt_{req.bookingId}"
    })
    return order

class VerifyPaymentRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str


@router.post("/verify-payment")
def verify_payment(req: VerifyPaymentRequest):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": req.order_id,
            "razorpay_payment_id": req.payment_id,
            "razorpay_signature": req.signature
        })
        return {"status": "success"}
    except:
        return {"status": "failed"}