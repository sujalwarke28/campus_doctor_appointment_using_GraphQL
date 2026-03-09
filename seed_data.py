"""Seed script to populate the database with sample data."""

from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models import Student, Doctor, Appointment, Prescription, Feedback, AppointmentStatus, Specialization


def seed_database():
    """Seed the database with sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Student).first():
            print("Database already has data. Skipping seed.")
            return

        # Create Students
        students = [
            Student(name="John Doe", email="john.doe@campus.edu"),
            Student(name="Jane Smith", email="jane.smith@campus.edu"),
            Student(name="Bob Johnson", email="bob.johnson@campus.edu"),
            Student(name="Alice Brown", email="alice.brown@campus.edu"),
            Student(name="Charlie Wilson", email="charlie.wilson@campus.edu"),
        ]
        db.add_all(students)
        db.commit()
        print(f"Created {len(students)} students")

        # Create Doctors
        doctors = [
            Doctor(name="Dr. Sarah Williams", specialization=Specialization.GENERAL),
            Doctor(name="Dr. Michael Chen", specialization=Specialization.GENERAL),
            Doctor(name="Dr. Emily Davis", specialization=Specialization.DENTIST),
            Doctor(name="Dr. James Miller", specialization=Specialization.DENTIST),
            Doctor(name="Dr. Lisa Anderson", specialization=Specialization.PSYCHOLOGIST),
            Doctor(name="Dr. Robert Taylor", specialization=Specialization.PSYCHOLOGIST),
        ]
        db.add_all(doctors)
        db.commit()
        print(f"Created {len(doctors)} doctors")

        # Create some appointments
        now = datetime.now()
        appointments = [
            Appointment(
                doctor_id=1,
                student_id=1,
                scheduled_time=now + timedelta(days=1, hours=10),
                status=AppointmentStatus.SCHEDULED
            ),
            Appointment(
                doctor_id=2,
                student_id=2,
                scheduled_time=now + timedelta(days=1, hours=14),
                status=AppointmentStatus.SCHEDULED
            ),
            Appointment(
                doctor_id=3,
                student_id=3,
                scheduled_time=now - timedelta(days=2),
                status=AppointmentStatus.COMPLETED
            ),
            Appointment(
                doctor_id=5,
                student_id=4,
                scheduled_time=now + timedelta(days=3, hours=11),
                status=AppointmentStatus.SCHEDULED
            ),
            Appointment(
                doctor_id=1,
                student_id=5,
                scheduled_time=now - timedelta(days=5),
                status=AppointmentStatus.COMPLETED
            ),
        ]
        db.add_all(appointments)
        db.commit()
        print(f"Created {len(appointments)} appointments")

        # Create prescriptions for completed appointments
        prescriptions = [
            Prescription(
                appointment_id=3,
                notes="Dental cleaning completed. No cavities found. Recommended flossing daily."
            ),
            Prescription(
                appointment_id=5,
                notes="Patient has mild flu symptoms. Prescribed rest and plenty of fluids. Follow up in 1 week if symptoms persist."
            ),
        ]
        db.add_all(prescriptions)
        db.commit()
        print(f"Created {len(prescriptions)} prescriptions")

        # Create feedback for completed appointments
        feedbacks = [
            Feedback(
                appointment_id=3,
                rating=5,
                comment="Very professional and gentle. Highly recommend!"
            ),
            Feedback(
                appointment_id=5,
                rating=4,
                comment="Good consultation, but had to wait a bit."
            ),
        ]
        db.add_all(feedbacks)
        db.commit()
        print(f"Created {len(feedbacks)} feedbacks")

        print("\nDatabase seeded successfully!")
        print("\nSample data created:")
        print("- 5 Students")
        print("- 6 Doctors (2 general, 2 dentist, 2 psychologist)")
        print("- 5 Appointments (3 scheduled, 2 completed)")
        print("- 2 Prescriptions")
        print("- 2 Feedbacks")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
