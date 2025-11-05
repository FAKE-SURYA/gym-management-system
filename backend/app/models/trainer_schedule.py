from sqlalchemy import Column, Integer, ForeignKey, Time, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class DayOfWeek(str, enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class TrainerSchedule(Base):
    __tablename__ = "trainer_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    trainer = relationship("User", back_populates="trainer_schedules")
