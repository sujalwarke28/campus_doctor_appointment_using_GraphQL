# Doctor Appointment Network - API Documentation & Test Cases

## Table of Contents
1. [Query Operations](#query-operations)
2. [Mutation Operations](#mutation-operations)
3. [Basic API Examples](#basic-api-examples)
4. [Test Cases with Sample Data](#test-cases-with-sample-data)

---

## Query Operations

| # | Operation | Description | Parameters |
|---|-----------|-------------|------------|
| 1 | `students` | Get all students | None |
| 2 | `student` | Get student by ID | `id: Int!` |
| 3 | `doctors` | Get all doctors (with optional filter) | `specialization: String` (optional) |
| 4 | `doctor` | Get doctor by ID | `id: Int!` |
| 5 | `appointments` | Get all appointments (with optional filters) | `status: String`, `studentId: Int`, `doctorId: Int` (all optional) |
| 6 | `appointment` | Get appointment by ID | `id: Int!` |
| 7 | `prescriptions` | Get all prescriptions | None |
| 8 | `feedbacks` | Get all feedbacks | None |
| 9 | `studentAppointmentHistory` | Get appointment history for a student | `studentId: Int!` |

## Mutation Operations

| # | Operation | Description | Input Fields |
|---|-----------|-------------|--------------|
| 1 | `createStudent` | Create a new student | `name: String!`, `email: String!` |
| 2 | `createDoctor` | Create a new doctor | `name: String!`, `specialization: String!` |
| 3 | `bookAppointment` | Book a new appointment | `doctorId: Int!`, `studentId: Int!`, `scheduledDate: String!` (YYYY-MM-DD), `scheduledTime: String!` (HH:MM) |
| 4 | `cancelAppointment` | Cancel an appointment | `appointmentId: Int!` |
| 5 | `completeAppointment` | Mark appointment as completed | `appointmentId: Int!` |
| 6 | `createPrescription` | Create prescription for appointment | `appointmentId: Int!`, `notes: String!` |
| 7 | `createFeedback` | Create feedback for appointment | `appointmentId: Int!`, `rating: Int!`, `comment: String` |
| 8 | `updatePrescription` | Update existing prescription | `id: Int!`, `notes: String!` |
| 9 | `deleteAppointment` | Delete an appointment | `id: Int!` |

---

## Basic API Examples

### 1. Create a Student

```graphql
mutation {
  createStudent(input: {
    name: "John Doe"
    email: "john.doe@campus.edu"
  }) {
    id
    name
    email
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createStudent": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@campus.edu"
    }
  }
}
```

---

### 2. Create a Doctor

```graphql
mutation {
  createDoctor(input: {
    name: "Dr. Sarah Williams"
    specialization: "general"
  }) {
    id
    name
    specialization
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createDoctor": {
      "id": 1,
      "name": "Dr. Sarah Williams",
      "specialization": "general"
    }
  }
}
```

**Note:** Valid specializations are: `general`, `dentist`, `psychologist`

---

### 3. Get All Students

```graphql
query {
  students {
    id
    name
    email
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "students": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@campus.edu"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@campus.edu"
      }
    ]
  }
}
```

---

### 4. Get All Doctors

```graphql
query {
  doctors {
    id
    name
    specialization
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "doctors": [
      {
        "id": 1,
        "name": "Dr. Sarah Williams",
        "specialization": "general"
      },
      {
        "id": 2,
        "name": "Dr. Michael Chen",
        "specialization": "general"
      },
      {
        "id": 3,
        "name": "Dr. Emily Davis",
        "specialization": "dentist"
      }
    ]
  }
}
```

---

### 5. Get Student by ID

```graphql
query {
  student(id: 1) {
    id
    name
    email
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "student": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@campus.edu"
    }
  }
}
```

---

### 6. Get Doctor by ID

```graphql
query {
  doctor(id: 1) {
    id
    name
    specialization
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "doctor": {
      "id": 1,
      "name": "Dr. Sarah Williams",
      "specialization": "general"
    }
  }
}
```

---

## Test Cases with Sample Data

### Test Case 1: Specialization Filter

**Description:** Filter doctors by their specialization

**Query:**
```graphql
query {
  doctors(specialization: "general") {
    id
    name
    specialization
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "doctors": [
      {
        "id": 1,
        "name": "Dr. Sarah Williams",
        "specialization": "general"
      },
      {
        "id": 2,
        "name": "Dr. Michael Chen",
        "specialization": "general"
      }
    ]
  }
}
```

**Additional Filter Tests:**
```graphql
# Get dentists
query {
  doctors(specialization: "dentist") {
    id
    name
    specialization
  }
}

# Get psychologists
query {
  doctors(specialization: "psychologist") {
    id
    name
    specialization
  }
}
```

---

### Test Case 2: Appointment Scheduling

**Description:** Book a new appointment for a student with a doctor

**Step 1 - Create a Student (if needed):**
```graphql
mutation {
  createStudent(input: {
    name: "Test Student"
    email: "test.student@campus.edu"
  }) {
    id
    name
    email
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createStudent": {
      "id": 6,
      "name": "Test Student",
      "email": "test.student@campus.edu"
    }
  }
}
```

**Step 2 - Book Appointment:**
```graphql
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
    doctor {
      name
      specialization
    }
    student {
      name
      email
    }
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "bookAppointment": {
      "id": 6,
      "scheduledDate": "2024-03-22",
      "scheduledTime": "15:00",
      "status": "scheduled",
      "doctor": {
        "name": "Dr. Sarah Williams",
        "specialization": "general"
      },
      "student": {
        "name": "John Doe",
        "email": "john.doe@campus.edu"
      }
    }
  }
}
```

---

### Test Case 3: Time Conflict Prevention

**Description:** Prevent booking when doctor already has an appointment within 30 minutes

**Step 1 - Book First Appointment:**
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 1
    scheduledDate: "2024-04-15"
    scheduledTime: "10:00"
  }) {
    id
    scheduledDate
    scheduledTime
  }
}
```

**Step 2 - Attempt Conflicting Appointment (within 30 minutes):**
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 2
    scheduledDate: "2024-04-15"
    scheduledTime: "10:15"
  }) {
    id
    scheduledDate
    scheduledTime
  }
}
```

**Expected Error Response:**
```json
{
  "data": null,
  "errors": [
    {
      "message": "Time conflict: Doctor already has an appointment scheduled around this time"
    }
  ]
}
```

**Step 3 - Book Non-Conflicting Appointment (more than 30 minutes later):**
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 2
    scheduledDate: "2024-04-15"
    scheduledTime: "11:00"
  }) {
    id
    scheduledDate
    scheduledTime
    status
  }
}
```

**Expected Success Response:**
```json
{
  "data": {
    "bookAppointment": {
      "id": 8,
      "scheduledDate": "2024-04-15",
      "scheduledTime": "11:00",
      "status": "scheduled"
    }
  }
}
```

---

### Test Case 4: Prescription Storage

**Description:** Create and store prescription for a completed appointment

**Step 1 - Complete an Appointment:**
```graphql
mutation {
  completeAppointment(appointmentId: 1) {
    id
    status
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "completeAppointment": {
      "id": 1,
      "status": "completed"
    }
  }
}
```

**Step 2 - Create Prescription:**
```graphql
mutation {
  createPrescription(input: {
    appointmentId: 1
    notes: "Patient diagnosed with common cold. Prescribed: Paracetamol 500mg twice daily for 5 days. Rest advised. Drink plenty of fluids. Follow up if symptoms persist after 1 week."
  }) {
    id
    appointmentId
    notes
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createPrescription": {
      "id": 3,
      "appointmentId": 1,
      "notes": "Patient diagnosed with common cold. Prescribed: Paracetamol 500mg twice daily for 5 days. Rest advised. Drink plenty of fluids. Follow up if symptoms persist after 1 week."
    }
  }
}
```

**Step 3 - Query Prescription:**
```graphql
query {
  prescriptions {
    id
    appointmentId
    notes
  }
}
```

**Step 4 - Update Prescription:**
```graphql
mutation {
  updatePrescription(
    id: 1
    notes: "Updated: Patient diagnosed with common cold. Prescribed: Paracetamol 500mg twice daily for 7 days (extended). Add Vitamin C supplements."
  ) {
    id
    notes
  }
}
```

---

### Test Case 5: Feedback Tracking

**Description:** Submit and track feedback for appointments

**Step 1 - Create Feedback with High Rating:**
```graphql
mutation {
  createFeedback(input: {
    appointmentId: 1
    rating: 5
    comment: "Excellent consultation! Dr. Williams was very thorough and caring. Highly recommend for general checkups."
  }) {
    id
    appointmentId
    rating
    comment
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createFeedback": {
      "id": 3,
      "appointmentId": 1,
      "rating": 5,
      "comment": "Excellent consultation! Dr. Williams was very thorough and caring. Highly recommend for general checkups."
    }
  }
}
```

**Step 2 - Create Feedback with Lower Rating:**
```graphql
mutation {
  createFeedback(input: {
    appointmentId: 2
    rating: 3
    comment: "Good consultation but had to wait 20 minutes past appointment time."
  }) {
    id
    appointmentId
    rating
    comment
  }
}
```

**Step 3 - Query All Feedbacks:**
```graphql
query {
  feedbacks {
    id
    appointmentId
    rating
    comment
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "feedbacks": [
      {
        "id": 1,
        "appointmentId": 3,
        "rating": 5,
        "comment": "Very professional and gentle. Highly recommend!"
      },
      {
        "id": 2,
        "appointmentId": 5,
        "rating": 4,
        "comment": "Good consultation, but had to wait a bit."
      }
    ]
  }
}
```

**Invalid Rating Test (should fail):**
```graphql
mutation {
  createFeedback(input: {
    appointmentId: 4
    rating: 6
    comment: "Invalid rating"
  }) {
    id
  }
}
```

**Expected Error:**
```json
{
  "data": null,
  "errors": [
    {
      "message": "Rating must be between 1 and 5"
    }
  ]
}
```

---

### Test Case 6: History Maintenance

**Description:** View and maintain appointment history for a student

**Query Student Appointment History:**
```graphql
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
    prescription {
      notes
    }
    feedback {
      rating
      comment
    }
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "studentAppointmentHistory": [
      {
        "id": 1,
        "scheduledDate": "2024-03-10",
        "scheduledTime": "10:00",
        "status": "scheduled",
        "doctor": {
          "name": "Dr. Sarah Williams",
          "specialization": "general"
        },
        "prescription": null,
        "feedback": null
      }
    ]
  }
}
```

**Query All Appointments with Filters:**
```graphql
# Get only scheduled appointments
query {
  appointments(status: "scheduled") {
    id
    scheduledDate
    scheduledTime
    status
    student {
      name
    }
    doctor {
      name
    }
  }
}

# Get only completed appointments
query {
  appointments(status: "completed") {
    id
    scheduledDate
    scheduledTime
    status
  }
}

# Get appointments for a specific doctor
query {
  appointments(doctorId: 1) {
    id
    scheduledDate
    scheduledTime
    status
    student {
      name
    }
  }
}
```

---

## Additional Test Cases

### Create Doctor Test
```graphql
mutation {
  createDoctor(input: {
    name: "Dr. Amanda Foster"
    specialization: "dentist"
  }) {
    id
    name
    specialization
  }
}
```

### Get Single Student Test
```graphql
query {
  student(id: 1) {
    id
    name
    email
  }
}
```

### Get Single Doctor Test
```graphql
query {
  doctor(id: 1) {
    id
    name
    specialization
  }
}
```

### Get Single Appointment with All Details
```graphql
query {
  appointment(id: 3) {
    id
    scheduledDate
    scheduledTime
    status
    doctor {
      id
      name
      specialization
    }
    student {
      id
      name
      email
    }
    prescription {
      id
      notes
    }
    feedback {
      id
      rating
      comment
    }
  }
}
```

### Cancel Appointment Test
```graphql
mutation {
  cancelAppointment(appointmentId: 4) {
    id
    status
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "cancelAppointment": {
      "id": 4,
      "status": "cancelled"
    }
  }
}
```

### Delete Appointment Test
```graphql
mutation {
  deleteAppointment(id: 5)
}
```

**Expected Response:**
```json
{
  "data": {
    "deleteAppointment": true
  }
}
```

---

## Error Handling Test Cases

### 1. Book Appointment with Non-Existent Doctor
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 999
    studentId: 1
    scheduledDate: "2024-03-25"
    scheduledTime: "10:00"
  }) {
    id
  }
}
```
**Expected Error:** "Doctor with ID 999 not found"

### 2. Book Appointment with Non-Existent Student
```graphql
mutation {
  bookAppointment(input: {
    doctorId: 1
    studentId: 999
    scheduledDate: "2024-03-25"
    scheduledTime: "10:00"
  }) {
    id
  }
}
```
**Expected Error:** "Student with ID 999 not found"

### 3. Create Duplicate Prescription
```graphql
mutation {
  createPrescription(input: {
    appointmentId: 3
    notes: "Duplicate prescription attempt"
  }) {
    id
  }
}
```
**Expected Error:** "Prescription already exists for appointment 3"

### 4. Create Duplicate Feedback
```graphql
mutation {
  createFeedback(input: {
    appointmentId: 3
    rating: 5
    comment: "Duplicate feedback attempt"
  }) {
    id
  }
}
```
**Expected Error:** "Feedback already exists for appointment 3"

### 5. Invalid Specialization
```graphql
mutation {
  createDoctor(input: {
    name: "Dr. Invalid"
    specialization: "cardiologist"
  }) {
    id
  }
}
```
**Expected Error:** "Invalid specialization. Must be one of: general, dentist, psychologist"

---

## Sample Data Reference

### Pre-seeded Students
| ID | Name | Email |
|----|------|-------|
| 1 | John Doe | john.doe@campus.edu |
| 2 | Jane Smith | jane.smith@campus.edu |
| 3 | Bob Johnson | bob.johnson@campus.edu |
| 4 | Alice Brown | alice.brown@campus.edu |
| 5 | Charlie Wilson | charlie.wilson@campus.edu |

### Pre-seeded Doctors
| ID | Name | Specialization |
|----|------|----------------|
| 1 | Dr. Sarah Williams | general |
| 2 | Dr. Michael Chen | general |
| 3 | Dr. Emily Davis | dentist |
| 4 | Dr. James Miller | dentist |
| 5 | Dr. Lisa Anderson | psychologist |
| 6 | Dr. Robert Taylor | psychologist |

### Appointment Status Values
- `scheduled` - Appointment is booked and upcoming
- `completed` - Appointment has been completed
- `cancelled` - Appointment was cancelled

### Specialization Values
- `general` - General practitioner
- `dentist` - Dental specialist
- `psychologist` - Mental health specialist

### Input Format Reference
- **scheduledDate**: `YYYY-MM-DD` (e.g., "2024-03-22")
- **scheduledTime**: `HH:MM` (e.g., "15:00" for 3:00 PM)

---

## Quick Test Script

Run these queries in sequence to test all functionality:

```graphql
# 1. Get all doctors
query { doctors { id name specialization } }

# 2. Filter by specialization
query { doctors(specialization: "general") { name } }

# 3. Get all students
query { students { id name email } }

# 4. Book an appointment
mutation { bookAppointment(input: { doctorId: 1, studentId: 1, scheduledDate: "2024-05-01", scheduledTime: "09:00" }) { id status } }

# 5. Get appointments
query { appointments { id scheduledDate scheduledTime status } }

# 6. Complete appointment
mutation { completeAppointment(appointmentId: 1) { id status } }

# 7. Add prescription
mutation { createPrescription(input: { appointmentId: 1, notes: "Test prescription" }) { id notes } }

# 8. Add feedback
mutation { createFeedback(input: { appointmentId: 1, rating: 5, comment: "Great!" }) { id rating } }

# 9. View history
query { studentAppointmentHistory(studentId: 1) { id status prescription { notes } feedback { rating } } }
```
