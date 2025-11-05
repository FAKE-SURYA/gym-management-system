from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    trainer = "trainer"
    member = "member"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.member)
    profile_image = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    memberships = relationship("Membership", back_populates="member", foreign_keys="Membership.member_id")
    trainer_memberships = relationship("Membership", back_populates="trainer", foreign_keys="Membership.trainer_id")
    payments = relationship("Payment", back_populates="member", cascade="all, delete-orphan")
    attendance = relationship("Attendance", back_populates="member", cascade="all, delete-orphan")
    trainer_schedules = relationship("TrainerSchedule", back_populates="trainer", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
