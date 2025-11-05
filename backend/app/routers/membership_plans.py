from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.membership_plan import MembershipPlan
from app.schemas.membership_plan import MembershipPlanCreate, MembershipPlanResponse
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/membership-plans", tags=["Membership Plans"])


@router.post("/", response_model=MembershipPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    payload: MembershipPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Create new membership plan (admin only)"""
    plan = MembershipPlan(**payload.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/", response_model=List[MembershipPlanResponse])
def get_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all membership plans"""
    plans = db.query(MembershipPlan).filter(MembershipPlan.is_active == True).offset(skip).limit(limit).all()
    return plans


@router.get("/{plan_id}", response_model=MembershipPlanResponse)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get membership plan details"""
    plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
