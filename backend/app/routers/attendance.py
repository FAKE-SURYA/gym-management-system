from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from app.database import get_db
from app.models.user import User
from app.models.attendance import Attendance
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/check-in", status_code=status.HTTP_201_CREATED)
def check_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Member check-in"""
    today = date.today()
    
    # Check if already checked in today
    existing = db.query(Attendance).filter(
        Attendance.member_id == current_user.id,
        Attendance.date == today,
        Attendance.check_out == None
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already checked in")
    
    attendance = Attendance(
        member_id=current_user.id,
        date=today
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return {"message": "Checked in successfully", "check_in": attendance.check_in}


@router.post("/check-out")
def check_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Member check-out"""
    today = date.today()
    
    attendance = db.query(Attendance).filter(
        Attendance.member_id == current_user.id,
        Attendance.date == today,
        Attendance.check_out == None
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=400, detail="No active check-in found")
    
    attendance.check_out = datetime.now()
    db.commit()
    
    return {"message": "Checked out successfully", "check_out": attendance.check_out}


@router.get("/history", response_model=List[dict])
def get_attendance_history(
    member_id: int = None,
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance history"""
    query = db.query(Attendance)
    
    # Members can only see their own attendance
    if current_user.role == "member":
        query = query.filter(Attendance.member_id == current_user.id)
    elif member_id:
        query = query.filter(Attendance.member_id == member_id)
    
    attendance_records = query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": record.id,
            "date": record.date,
            "check_in": record.check_in,
            "check_out": record.check_out,
            "member_id": record.member_id
        }
        for record in attendance_records
    ]
