from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
import razorpay
import hmac
import hashlib
from app.database import get_db
from app.config import get_settings
from app.models.user import User
from app.models.payment import Payment, PaymentStatus
from app.models.membership import Membership, MembershipStatus
from app.schemas.payment import PaymentResponse
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/payments", tags=["Payments"])
settings = get_settings()

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@router.post("/create-order")
def create_payment_order(
    membership_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create Razorpay order for membership payment"""
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    # Members can only pay for their own memberships
    if current_user.role == "member" and membership.member_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot pay for other member's membership")
    
    # Calculate amount
    amount = int(float(membership.plan.price) * 100)  # Convert to paise
    
    # Create Razorpay order
    order_data = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"membership_{membership_id}",
        "notes": {
            "membership_id": membership_id,
            "member_id": current_user.id
        }
    }
    
    razorpay_order = razorpay_client.order.create(data=order_data)
    
    # Create payment record
    payment = Payment(
        membership_id=membership_id,
        member_id=current_user.id,
        amount=membership.plan.price,
        payment_method="razorpay",
        razorpay_order_id=razorpay_order["id"],
        status=PaymentStatus.pending
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return {
        "order_id": razorpay_order["id"],
        "amount": razorpay_order["amount"],
        "currency": razorpay_order["currency"],
        "key_id": settings.RAZORPAY_KEY_ID,
        "payment_id": payment.id
    }


@router.post("/verify-payment")
def verify_payment(
    request_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify Razorpay payment signature"""
    razorpay_order_id = request_data.get("razorpay_order_id")
    razorpay_payment_id = request_data.get("razorpay_payment_id")
    razorpay_signature = request_data.get("razorpay_signature")
    
    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        raise HTTPException(status_code=400, detail="Missing payment details")
    
    # Verify signature
    generated_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()
    
    if generated_signature != razorpay_signature:
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    # Update payment status
    payment = db.query(Payment).filter(Payment.razorpay_order_id == razorpay_order_id).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = PaymentStatus.completed
    payment.razorpay_payment_id = razorpay_payment_id
    payment.razorpay_signature = razorpay_signature
    
    # Activate membership
    membership = db.query(Membership).filter(Membership.id == payment.membership_id).first()
    if membership:
        membership.status = MembershipStatus.active
    
    db.commit()
    
    return {"status": "success", "message": "Payment verified successfully"}


@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    member_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all payments"""
    query = db.query(Payment)
    
    # Members can only see their own payments
    if current_user.role == "member":
        query = query.filter(Payment.member_id == current_user.id)
    elif member_id:
        query = query.filter(Payment.member_id == member_id)
    
    payments = query.offset(skip).limit(limit).all()
    return payments


@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Razorpay webhooks"""
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    # Verify webhook signature
    try:
        razorpay_client.utility.verify_webhook_signature(
            body.decode(),
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
    # Process event
    event_data = await request.json()
    event = event_data.get("event")
    
    if event == "payment.captured":
        payment_entity = event_data["payload"]["payment"]["entity"]
        order_id = payment_entity.get("order_id")
        payment_id = payment_entity.get("id")
        
        payment = db.query(Payment).filter(Payment.razorpay_order_id == order_id).first()
        if payment:
            payment.status = PaymentStatus.completed
            payment.razorpay_payment_id = payment_id
            db.commit()
    
    return {"status": "ok"}
