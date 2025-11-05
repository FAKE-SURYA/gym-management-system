from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.payment import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    membership_id: int
    amount: Decimal
    payment_method: PaymentMethod


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    transaction_id: Optional[str] = None
    status: PaymentStatus
    payment_date: datetime
    
    class Config:
        from_attributes = True
