from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.user import User
from app.models.membership import Membership, MembershipStatus
from app.schemas.membership import MembershipCreate, MembershipResponse
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post("/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def create_membership(
    payload: MembershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Create new membership (admin only)"""
    membership = Membership(**payload.dict())
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/", response_model=List[MembershipResponse])
def get_memberships(
    member_id: int = None,
    status: MembershipStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all memberships with optional filters"""
    query = db.query(Membership)
    
    # Members can only see their own memberships
    if current_user.role == "member":
        query = query.filter(Membership.member_id == current_user.id)
    elif member_id:
        query = query.filter(Membership.member_id == member_id)
    
    if status:
        query = query.filter(Membership.status == status)
    
    memberships = query.offset(skip).limit(limit).all()
    return memberships


@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership(
    membership_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get membership details"""
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    # Members can only view their own memberships
    if current_user.role == "member" and membership.member_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot view other member's membership")
    
    return membership


@router.put("/{membership_id}/status", response_model=MembershipResponse)
def update_membership_status(
    membership_id: int,
    new_status: MembershipStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Update membership status (admin only)"""
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    membership.status = new_status
    db.commit()
    db.refresh(membership)
    
    return membership


@router.get("/expiring/soon", response_model=List[MembershipResponse])
def get_expiring_memberships(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get memberships expiring within specified days"""
    from datetime import timedelta
    
    today = date.today()
    target_date = today + timedelta(days=days)
    
    memberships = db.query(Membership).filter(
        Membership.end_date >= today,
        Membership.end_date <= target_date,
        Membership.status == MembershipStatus.active
    ).all()
    
    return memberships
