from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.core.security import require_role

router = APIRouter(prefix="/trainers", tags=["Trainers"])


@router.get("/", response_model=List[UserResponse])
def get_all_trainers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get all trainers (admin only)"""
    trainers = db.query(User).filter(User.role == UserRole.trainer).offset(skip).limit(limit).all()
    return trainers


@router.get("/{trainer_id}", response_model=UserResponse)
def get_trainer(
    trainer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get trainer details"""
    trainer = db.query(User).filter(User.id == trainer_id, User.role == UserRole.trainer).first()
    
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    
    return trainer
