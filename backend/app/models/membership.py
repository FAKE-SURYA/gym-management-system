from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MembershipStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    suspended = "suspended"
    cancelled = "cancelled"


class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("membership_plans.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False, index=True)
    status = Column(Enum(MembershipStatus), default=MembershipStatus.active, index=True)
    auto_renew = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("User", back_populates="memberships", foreign_keys=[member_id])
    trainer = relationship("User", back_populates="trainer_memberships", foreign_keys=[trainer_id])
    plan = relationship("MembershipPlan", back_populates="memberships")
    payments = relationship("Payment", back_populates="membership", cascade="all, delete-orphan")
