from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.membership import Membership, MembershipStatus
from app.models.user import User
from app.models.notification import Notification, NotificationType
from app.core.email import send_email
from app.core.sms import send_sms


def check_expiring_memberships():
    """
    Background task to check expiring memberships and send notifications.
    Run this daily via cron or APScheduler.
    """
    db = SessionLocal()
    try:
        # Get memberships expiring in 3 days
        target_date = date.today() + timedelta(days=3)
        
        expiring = db.query(Membership).filter(
            Membership.end_date == target_date,
            Membership.status == MembershipStatus.active
        ).all()
        
        for membership in expiring:
            member = db.query(User).filter(User.id == membership.member_id).first()
            
            if not member:
                continue
            
            # Create notification
            notification = Notification(
                user_id=member.id,
                title="Membership Expiring Soon",
                message=f"Your membership expires on {membership.end_date.strftime('%B %d, %Y')}. Renew now to continue!",
                notification_type=NotificationType.membership_expiry
            )
            db.add(notification)
            
            # Send email
            send_email(
                to=member.email,
                subject="Your Gym Membership Expires in 3 Days",
                body=f"""Hi {member.full_name},

Your gym membership expires on {membership.end_date.strftime('%B %d, %Y')}.

Renew now to continue enjoying our facilities!

Best regards,
Gym Management Team"""
            )
            
            # Send SMS (optional)
            if member.phone:
                send_sms(
                    to=member.phone,
                    message=f"Hi {member.full_name}, your gym membership expires in 3 days. Renew now!"
                )
        
        db.commit()
        print(f"Processed {len(expiring)} expiring memberships")
        
    except Exception as e:
        print(f"Error in expiry checker: {e}")
        db.rollback()
    finally:
        db.close()


def update_expired_memberships():
    """Update status of expired memberships"""
    db = SessionLocal()
    try:
        today = date.today()
        
        expired = db.query(Membership).filter(
            Membership.end_date < today,
            Membership.status == MembershipStatus.active
        ).all()
        
        for membership in expired:
            membership.status = MembershipStatus.expired
        
        db.commit()
        print(f"Updated {len(expired)} expired memberships")
        
    except Exception as e:
        print(f"Error updating expired memberships: {e}")
        db.rollback()
    finally:
        db.close()
