from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PlanType(str, enum.Enum):
    strength = "strength"
    weight_loss = "weight_loss"
    cardio = "cardio"
    personal_training = "personal_training"
    general = "general"


class MembershipPlan(Base):
    __tablename__ = "membership_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    plan_type = Column(Enum(PlanType), nullable=False)
    duration_months = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    features = Column(JSON, nullable=True)  # Store as JSON array
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    memberships = relationship("Membership", back_populates="plan")
