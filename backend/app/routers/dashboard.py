from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta, date
from app.database import get_db
from app.models.user import User, UserRole
from app.models.membership import Membership, MembershipStatus
from app.models.payment import Payment, PaymentStatus
from app.models.attendance import Attendance
from app.core.security import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get admin dashboard statistics"""
    today = date.today()
    this_month_start = today.replace(day=1)
    
    # Total active members
    active_members = db.query(func.count(Membership.id)).filter(
        Membership.status == MembershipStatus.active
    ).scalar()
    
    # Memberships expiring in next 7 days
    expiring_soon = db.query(func.count(Membership.id)).filter(
        and_(
            Membership.end_date >= today,
            Membership.end_date <= today + timedelta(days=7),
            Membership.status == MembershipStatus.active
        )
    ).scalar()
    
    # Revenue this month
    monthly_revenue = db.query(func.sum(Payment.amount)).filter(
        and_(
            Payment.payment_date >= this_month_start,
            Payment.status == PaymentStatus.completed
        )
    ).scalar() or 0
    
    # Today's attendance
    today_attendance = db.query(func.count(Attendance.id)).filter(
        Attendance.date == today
    ).scalar()
    
    # New members this month
    new_members = db.query(func.count(User.id)).filter(
        and_(
            User.role == UserRole.member,
            User.created_at >= this_month_start
        )
    ).scalar()
    
    # Revenue trend (last 6 months)
    revenue_trend = []
    for i in range(6):
        month_start = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_revenue = db.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.payment_date >= month_start,
                Payment.payment_date <= month_end,
                Payment.status == PaymentStatus.completed
            )
        ).scalar() or 0
        
        revenue_trend.insert(0, {
            "month": month_start.strftime("%B"),
            "revenue": float(month_revenue)
        })
    
    return {
        "active_members": active_members,
        "expiring_soon": expiring_soon,
        "monthly_revenue": float(monthly_revenue),
        "today_attendance": today_attendance,
        "new_members_this_month": new_members,
        "revenue_trend": revenue_trend
    }
