from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.membership_plan import PlanType


class MembershipPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    plan_type: PlanType
    duration_months: int
    price: Decimal
    features: Optional[List[str]] = None
    
    @validator('duration_months')
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v


class MembershipPlanCreate(MembershipPlanBase):
    pass


class MembershipPlanResponse(MembershipPlanBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
