from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

# Simple password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Check if admin exists
existing = db.query(User).filter(User.email == "admin@gym.com").first()

if existing:
    print("❌ Admin already exists!")
else:
    # Hash password
    hashed = pwd_context.hash("admin123")
    
    # Create admin
    admin = User(
        email="admin@gym.com",
        password_hash=hashed,
        full_name="Admin User",
        phone="9876543210",
        role="admin",
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    print("✅ Admin created successfully!")
    print("📧 Email: admin@gym.com")
    print("🔑 Password: admin123")

db.close()
