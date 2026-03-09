import strawberry
from strawberry.types import Info
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database import SessionLocal
from models import (
    Student as StudentModel,
    Doctor as DoctorModel,
    Appointment as AppointmentModel,
    Prescription as PrescriptionModel,
    Feedback as FeedbackModel,
    AppointmentStatus,
    Specialization,
)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass


# ----- GraphQL Types -----

@strawberry.type
class PrescriptionType:
    """Prescription GraphQL type."""
    id: int
    appointment_id: int
    notes: str


@strawberry.type
class FeedbackType:
    """Feedback GraphQL type."""
    id: int
    appointment_id: int
    rating: int
    comment: Optional[str]


@strawberry.type
class StudentType:
    """Student GraphQL type."""
    id: int
    name: str
    email: str


@strawberry.type
class DoctorType:
    """Doctor GraphQL type."""
    id: int
    name: str
    specialization: str


@strawberry.type
class AppointmentType:
    """Appointment GraphQL type."""
    id: int
    doctor_id: int
    student_id: int
    scheduled_date: str
    scheduled_time: str
    status: str
    doctor: Optional[DoctorType] = None
    student: Optional[StudentType] = None
    prescription: Optional[PrescriptionType] = None
    feedback: Optional[FeedbackType] = None


# ----- Input Types -----

@strawberry.input
class BookAppointmentInput:
    """Input for booking appointment."""
    doctor_id: int
    student_id: int
    scheduled_date: str  # Format: YYYY-MM-DD
    scheduled_time: str  # Format: HH:MM


@strawberry.input
class CreateStudentInput:
    """Input for creating student."""
    name: str
    email: str


@strawberry.input
class CreateDoctorInput:
    """Input for creating doctor."""
    name: str
    specialization: str


@strawberry.input
class CreatePrescriptionInput:
    """Input for creating prescription."""
    appointment_id: int
    notes: str


@strawberry.input
class CreateFeedbackInput:
    """Input for creating feedback."""
    appointment_id: int
    rating: int
    comment: Optional[str] = None


# ----- Helper Functions -----

def convert_student(student: StudentModel) -> StudentType:
    """Convert SQLAlchemy Student to GraphQL type."""
    return StudentType(
        id=student.id,
        name=student.name,
        email=student.email
    )


def convert_doctor(doctor: DoctorModel) -> DoctorType:
    """Convert SQLAlchemy Doctor to GraphQL type."""
    return DoctorType(
        id=doctor.id,
        name=doctor.name,
        specialization=doctor.specialization.value
    )


def convert_prescription(prescription: PrescriptionModel) -> PrescriptionType:
    """Convert SQLAlchemy Prescription to GraphQL type."""
    return PrescriptionType(
        id=prescription.id,
        appointment_id=prescription.appointment_id,
        notes=prescription.notes
    )


def convert_feedback(feedback: FeedbackModel) -> FeedbackType:
    """Convert SQLAlchemy Feedback to GraphQL type."""
    return FeedbackType(
        id=feedback.id,
        appointment_id=feedback.appointment_id,
        rating=feedback.rating,
        comment=feedback.comment
    )


def convert_appointment(appointment: AppointmentModel) -> AppointmentType:
    """Convert SQLAlchemy Appointment to GraphQL type."""
    return AppointmentType(
        id=appointment.id,
        doctor_id=appointment.doctor_id,
        student_id=appointment.student_id,
        scheduled_date=appointment.scheduled_time.strftime("%Y-%m-%d"),
        scheduled_time=appointment.scheduled_time.strftime("%H:%M"),
        status=appointment.status.value,
        doctor=convert_doctor(appointment.doctor) if appointment.doctor else None,
        student=convert_student(appointment.student) if appointment.student else None,
        prescription=convert_prescription(appointment.prescription) if appointment.prescription else None,
        feedback=convert_feedback(appointment.feedback) if appointment.feedback else None
    )


def check_time_conflict(db: Session, doctor_id: int, scheduled_time: datetime, exclude_appointment_id: int = None) -> bool:
    """Check if there's a time conflict for the doctor."""
    # Appointments are assumed to be 30 minutes long
    time_window = timedelta(minutes=30)
    start_time = scheduled_time - time_window
    end_time = scheduled_time + time_window

    query = db.query(AppointmentModel).filter(
        AppointmentModel.doctor_id == doctor_id,
        AppointmentModel.status == AppointmentStatus.SCHEDULED,
        AppointmentModel.scheduled_time >= start_time,
        AppointmentModel.scheduled_time <= end_time
    )

    if exclude_appointment_id:
        query = query.filter(AppointmentModel.id != exclude_appointment_id)

    return query.first() is not None


# ----- Query -----

@strawberry.type
class Query:
    """GraphQL Query type."""

    @strawberry.field
    def students(self) -> List[StudentType]:
        """Get all students."""
        db = SessionLocal()
        try:
            students = db.query(StudentModel).all()
            return [convert_student(s) for s in students]
        finally:
            db.close()

    @strawberry.field
    def student(self, id: int) -> Optional[StudentType]:
        """Get student by ID."""
        db = SessionLocal()
        try:
            student = db.query(StudentModel).filter(StudentModel.id == id).first()
            return convert_student(student) if student else None
        finally:
            db.close()

    @strawberry.field
    def doctors(self, specialization: Optional[str] = None) -> List[DoctorType]:
        """Get all doctors, optionally filtered by specialization."""
        db = SessionLocal()
        try:
            query = db.query(DoctorModel)
            if specialization:
                try:
                    spec = Specialization(specialization.lower())
                    query = query.filter(DoctorModel.specialization == spec)
                except ValueError:
                    return []
            doctors = query.all()
            return [convert_doctor(d) for d in doctors]
        finally:
            db.close()

    @strawberry.field
    def doctor(self, id: int) -> Optional[DoctorType]:
        """Get doctor by ID."""
        db = SessionLocal()
        try:
            doctor = db.query(DoctorModel).filter(DoctorModel.id == id).first()
            return convert_doctor(doctor) if doctor else None
        finally:
            db.close()

    @strawberry.field
    def appointments(self, status: Optional[str] = None, student_id: Optional[int] = None, doctor_id: Optional[int] = None) -> List[AppointmentType]:
        """Get all appointments with optional filters."""
        db = SessionLocal()
        try:
            query = db.query(AppointmentModel)
            if status:
                try:
                    stat = AppointmentStatus(status.lower())
                    query = query.filter(AppointmentModel.status == stat)
                except ValueError:
                    return []
            if student_id:
                query = query.filter(AppointmentModel.student_id == student_id)
            if doctor_id:
                query = query.filter(AppointmentModel.doctor_id == doctor_id)
            appointments = query.order_by(AppointmentModel.scheduled_time.desc()).all()
            return [convert_appointment(a) for a in appointments]
        finally:
            db.close()

    @strawberry.field
    def appointment(self, id: int) -> Optional[AppointmentType]:
        """Get appointment by ID."""
        db = SessionLocal()
        try:
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
            return convert_appointment(appointment) if appointment else None
        finally:
            db.close()

    @strawberry.field
    def prescriptions(self) -> List[PrescriptionType]:
        """Get all prescriptions."""
        db = SessionLocal()
        try:
            prescriptions = db.query(PrescriptionModel).all()
            return [convert_prescription(p) for p in prescriptions]
        finally:
            db.close()

    @strawberry.field
    def feedbacks(self) -> List[FeedbackType]:
        """Get all feedbacks."""
        db = SessionLocal()
        try:
            feedbacks = db.query(FeedbackModel).all()
            return [convert_feedback(f) for f in feedbacks]
        finally:
            db.close()

    @strawberry.field
    def student_appointment_history(self, student_id: int) -> List[AppointmentType]:
        """Get appointment history for a student."""
        db = SessionLocal()
        try:
            appointments = db.query(AppointmentModel).filter(
                AppointmentModel.student_id == student_id
            ).order_by(AppointmentModel.scheduled_time.desc()).all()
            return [convert_appointment(a) for a in appointments]
        finally:
            db.close()


# ----- Mutation -----

@strawberry.type
class Mutation:
    """GraphQL Mutation type."""

    @strawberry.mutation
    def create_student(self, input: CreateStudentInput) -> StudentType:
        """Create a new student."""
        db = SessionLocal()
        try:
            student = StudentModel(name=input.name, email=input.email)
            db.add(student)
            db.commit()
            db.refresh(student)
            return convert_student(student)
        finally:
            db.close()

    @strawberry.mutation
    def create_doctor(self, input: CreateDoctorInput) -> DoctorType:
        """Create a new doctor."""
        db = SessionLocal()
        try:
            specialization = Specialization(input.specialization.lower())
            doctor = DoctorModel(name=input.name, specialization=specialization)
            db.add(doctor)
            db.commit()
            db.refresh(doctor)
            return convert_doctor(doctor)
        except ValueError:
            raise ValueError(f"Invalid specialization. Must be one of: general, dentist, psychologist")
        finally:
            db.close()

    @strawberry.mutation
    def book_appointment(self, input: BookAppointmentInput) -> AppointmentType:
        """Book a new appointment with time conflict prevention."""
        db = SessionLocal()
        try:
            # Parse scheduled date and time
            datetime_str = f"{input.scheduled_date}T{input.scheduled_time}:00"
            scheduled_time = datetime.fromisoformat(datetime_str)

            # Check if doctor exists
            doctor = db.query(DoctorModel).filter(DoctorModel.id == input.doctor_id).first()
            if not doctor:
                raise ValueError(f"Doctor with ID {input.doctor_id} not found")

            # Check if student exists
            student = db.query(StudentModel).filter(StudentModel.id == input.student_id).first()
            if not student:
                raise ValueError(f"Student with ID {input.student_id} not found")

            # Check for time conflicts
            if check_time_conflict(db, input.doctor_id, scheduled_time):
                raise ValueError("Time conflict: Doctor already has an appointment scheduled around this time")

            appointment = AppointmentModel(
                doctor_id=input.doctor_id,
                student_id=input.student_id,
                scheduled_time=scheduled_time,
                status=AppointmentStatus.SCHEDULED
            )
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            return convert_appointment(appointment)
        finally:
            db.close()

    @strawberry.mutation
    def cancel_appointment(self, appointment_id: int) -> AppointmentType:
        """Cancel an appointment."""
        db = SessionLocal()
        try:
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
            if not appointment:
                raise ValueError(f"Appointment with ID {appointment_id} not found")
            
            appointment.status = AppointmentStatus.CANCELLED
            db.commit()
            db.refresh(appointment)
            return convert_appointment(appointment)
        finally:
            db.close()

    @strawberry.mutation
    def complete_appointment(self, appointment_id: int) -> AppointmentType:
        """Mark an appointment as completed."""
        db = SessionLocal()
        try:
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
            if not appointment:
                raise ValueError(f"Appointment with ID {appointment_id} not found")
            
            appointment.status = AppointmentStatus.COMPLETED
            db.commit()
            db.refresh(appointment)
            return convert_appointment(appointment)
        finally:
            db.close()

    @strawberry.mutation
    def create_prescription(self, input: CreatePrescriptionInput) -> PrescriptionType:
        """Create a prescription for an appointment."""
        db = SessionLocal()
        try:
            # Check if appointment exists
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == input.appointment_id).first()
            if not appointment:
                raise ValueError(f"Appointment with ID {input.appointment_id} not found")

            # Check if prescription already exists
            existing = db.query(PrescriptionModel).filter(PrescriptionModel.appointment_id == input.appointment_id).first()
            if existing:
                raise ValueError(f"Prescription already exists for appointment {input.appointment_id}")

            prescription = PrescriptionModel(
                appointment_id=input.appointment_id,
                notes=input.notes
            )
            db.add(prescription)
            db.commit()
            db.refresh(prescription)
            return convert_prescription(prescription)
        finally:
            db.close()

    @strawberry.mutation
    def create_feedback(self, input: CreateFeedbackInput) -> FeedbackType:
        """Create feedback for an appointment."""
        db = SessionLocal()
        try:
            # Validate rating
            if input.rating < 1 or input.rating > 5:
                raise ValueError("Rating must be between 1 and 5")

            # Check if appointment exists
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == input.appointment_id).first()
            if not appointment:
                raise ValueError(f"Appointment with ID {input.appointment_id} not found")

            # Check if feedback already exists
            existing = db.query(FeedbackModel).filter(FeedbackModel.appointment_id == input.appointment_id).first()
            if existing:
                raise ValueError(f"Feedback already exists for appointment {input.appointment_id}")

            feedback = FeedbackModel(
                appointment_id=input.appointment_id,
                rating=input.rating,
                comment=input.comment
            )
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            return convert_feedback(feedback)
        finally:
            db.close()

    @strawberry.mutation
    def update_prescription(self, id: int, notes: str) -> PrescriptionType:
        """Update a prescription."""
        db = SessionLocal()
        try:
            prescription = db.query(PrescriptionModel).filter(PrescriptionModel.id == id).first()
            if not prescription:
                raise ValueError(f"Prescription with ID {id} not found")
            
            prescription.notes = notes
            db.commit()
            db.refresh(prescription)
            return convert_prescription(prescription)
        finally:
            db.close()

    @strawberry.mutation
    def delete_appointment(self, id: int) -> bool:
        """Delete an appointment."""
        db = SessionLocal()
        try:
            appointment = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
            if not appointment:
                raise ValueError(f"Appointment with ID {id} not found")
            
            db.delete(appointment)
            db.commit()
            return True
        finally:
            db.close()


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
