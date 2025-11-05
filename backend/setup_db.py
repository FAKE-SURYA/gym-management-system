from app.database import init_db, Base, engine
from app.models import (
    User, 
    MembershipPlan, 
    Membership, 
    Payment, 
    Attendance, 
    TrainerSchedule, 
    Notification
)

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
