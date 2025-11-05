from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime
from app.models.membership import MembershipStatus


class MembershipBase(BaseModel):
    member_id: int
    plan_id: int
    trainer_id: Optional[int] = None
    start_date: date
    end_date: date
    auto_renew: bool = False
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class MembershipCreate(MembershipBase):
    pass


class MembershipResponse(MembershipBase):
    id: int
    status: MembershipStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
