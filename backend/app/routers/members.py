from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[UserResponse])
def get_all_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "trainer"]))
):
    """Get all members (admin/trainer only)"""
    members = db.query(User).filter(User.role == UserRole.member).offset(skip).limit(limit).all()
    return members


@router.get("/{member_id}", response_model=UserResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get member details"""
    # Members can only view their own profile
    if current_user.role == UserRole.member and current_user.id != member_id:
        raise HTTPException(status_code=403, detail="Cannot view other member's profile")
    
    member = db.query(User).filter(User.id == member_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return member


@router.put("/{member_id}", response_model=UserResponse)
def update_member(
    member_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update member details"""
    # Members can only update their own profile
    if current_user.role == UserRole.member and current_user.id != member_id:
        raise HTTPException(status_code=403, detail="Cannot update other member's profile")
    
    member = db.query(User).filter(User.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Update fields
    if payload.full_name:
        member.full_name = payload.full_name
    if payload.phone:
        member.phone = payload.phone
    if payload.profile_image:
        member.profile_image = payload.profile_image
    
    db.commit()
    db.refresh(member)
    
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Delete member (admin only)"""
    member = db.query(User).filter(User.id == member_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    
    return None
