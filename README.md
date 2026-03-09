# Doctor Appointment Network

A GraphQL API for students to book campus medical appointments, built with FastAPI, Strawberry GraphQL, and SQLite.

## Features

- **Student Management**: Register and manage student profiles
- **Doctor Management**: Doctors with specializations (general, dentist, psychologist)
- **Appointment Booking**: Book appointments with time conflict prevention
- **Prescription Storage**: Store prescriptions for completed appointments
- **Feedback System**: Rate and comment on appointments
- **History Tracking**: View appointment history by student

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Strawberry GraphQL**: Python GraphQL library
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database
- **GraphiQL**: Interactive GraphQL IDE

## Setup

1. **Create a virtual environment**:
   ```bash
   cd doctor_appointment_network
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Seed the database** (optional, for sample data):
   ```bash
   python seed_data.py
   ```

4. **Run the server**:
   ```bash
   python main.py
   # OR
   uvicorn main:app --reload
   ```

5. **Access GraphiQL Interface**:
   Open http://localhost:8000/graphql in your browser

## Database Models

- **Student**: id, name, email
- **Doctor**: id, name, specialization (general, dentist, psychologist)
- **Appointment**: id, doctor_id, student_id, scheduled_date, scheduled_time, status (scheduled, completed, cancelled)
- **Prescription**: id, appointment_id, notes
- **Feedback**: id, appointment_id, rating, comment

## GraphQL API

### Queries

```graphql
# Get all doctors (optionally filter by specialization)
query {
  doctors(specialization: "general") {
    id
    name
    specialization
  }
}

# Get all students
query {
  students {
    id
    name
    email
  }
}

# Get all appointments
query {
  appointments(status: "scheduled") {
    id
    scheduledDate
    scheduledTime
    status
    doctor {
      name
    }
    student {
      name
    }
  }
}

# Get appointment by ID
query {
  appointment(id: 1) {
    id
    scheduledDate
    scheduledTime
    status
    prescription {
      notes
    }
    feedback {
      rating
      comment
    }
  }
}

# Get student appointment history
query {
  studentAppointmentHistory(studentId: 1) {
    id
    scheduledDate
    scheduledTime
    status
    doctor {
      name
      specialization
    }
  }
}

# Get all prescriptions
query {
  prescriptions {
    id
    appointmentId
    notes
  }
}

# Get all feedbacks
query {
  feedbacks {
    id
    rating
    comment
  }
}
```

### Mutations

```graphql
# Create a student
mutation {
  createStudent(input: { name: "Test Student", email: "test@campus.edu" }) {
    id
    name
    email
  }
}

# Create a doctor
mutation {
  createDoctor(input: { name: "Dr. New Doctor", specialization: "general" }) {
    id
    name
    specialization
  }
}

# Book an appointment
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 1
    scheduledDate: "2024-03-22"
    scheduledTime: "15:00"
  }) {
    id
    scheduledDate
    scheduledTime
    status
  }
}

# Cancel an appointment
mutation {
  cancelAppointment(appointmentId: 1) {
    id
    status
  }
}

# Complete an appointment
mutation {
  completeAppointment(appointmentId: 1) {
    id
    status
  }
}

# Create a prescription
mutation {
  createPrescription(input: {
    appointmentId: 1
    notes: "Take medication twice daily for 7 days."
  }) {
    id
    notes
  }
}

# Create feedback
mutation {
  createFeedback(input: {
    appointmentId: 1
    rating: 5
    comment: "Excellent service!"
  }) {
    id
    rating
    comment
  }
}

# Update prescription
mutation {
  updatePrescription(id: 1, notes: "Updated prescription notes") {
    id
    notes
  }
}

# Delete an appointment
mutation {
  deleteAppointment(id: 1)
}
```

## Test Cases Covered

1. **Specialization Filter**: Query doctors by specialization (general, dentist, psychologist)
2. **Appointment Scheduling**: Book appointments with doctor and student IDs
3. **Time Conflict Prevention**: Prevents booking if doctor has an appointment within 30 minutes
4. **Prescription Storage**: Create and update prescriptions for appointments
5. **Feedback Tracking**: Submit ratings (1-5) and comments for appointments
6. **History Maintenance**: View all appointments for a specific student

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /graphql` - GraphiQL interface
- `POST /graphql` - GraphQL endpoint

## Example Test Queries (As per Requirements)

### Test Query
```graphql
query {
  doctors(specialization: "general") {
    name
  }
}
```

### Test Mutation
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 1
    scheduledDate: "2024-03-22"
    scheduledTime: "15:00"
  }) {
    id
  }
}
```
