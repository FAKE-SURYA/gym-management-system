from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PaymentMethod(str, enum.Enum):
    razorpay = "razorpay"
    stripe = "stripe"
    cash = "cash"
    card = "card"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(Integer, ForeignKey("memberships.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, index=True)
    razorpay_order_id = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(255), nullable=True)
    razorpay_signature = Column(String(500), nullable=True)
    payment_metadata = Column(JSON, nullable=True)  # ✅ Changed from 'metadata'
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    membership = relationship("Membership", back_populates="payments")
    member = relationship("User", back_populates="payments")
