from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import enum


class AppointmentStatus(enum.Enum):
    """Enum for appointment status."""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Specialization(enum.Enum):
    """Enum for doctor specialization."""
    GENERAL = "general"
    DENTIST = "dentist"
    PSYCHOLOGIST = "psychologist"


class Student(Base):
    """Student model."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="student")


class Doctor(Base):
    """Doctor model."""
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(SQLEnum(Specialization), nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    """Appointment model."""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)

    # Relationships
    doctor = relationship("Doctor", back_populates="appointments")
    student = relationship("Student", back_populates="appointments")
    prescription = relationship("Prescription", back_populates="appointment", uselist=False)
    feedback = relationship("Feedback", back_populates="appointment", uselist=False)


class Prescription(Base):
    """Prescription model."""
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    notes = Column(String(1000), nullable=False)

    # Relationships
    appointment = relationship("Appointment", back_populates="prescription")


class Feedback(Base):
    """Feedback model."""
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String(500))

    # Relationships
    appointment = relationship("Appointment", back_populates="feedback")
