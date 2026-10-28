# Clinic Appointments — Use Cases

## Actors

| Actor | Description |
|-------|-------------|
| Patient | Person booking appointments with doctors |
| Doctor | Medical staff who accept/decline appointment requests |

*Note:* The system performs assignments itself, so the system is **not** an actor.

## Use Cases

| UC | Name | Actor | Requirement | Use Case Text |
|----|------|-------|-------------|---------------|
| UC1 | View Doctor Availability | Patient | R1 | As a Patient, I can view the days and times when a doctor is available. **Main flow:** 1. Patient opens the doctor's profile or schedule. 2. Patient requests the availability. 3. System displays the days and times when the doctor is available. 4. Patient reads the availability. **Alternative flow:** 3a. Doctor has no available days/times → system displays "No availability" instead of a list. |
| UC2 | Book Appointment | Patient | R2 | As a Patient, I can book an appointment during an available time slot. **Main flow:** 1. Patient selects an available time slot (from UC1). 2. Patient confirms the booking. 3. System books the appointment in that slot. 4. System sends the booking as a request to the doctor. **Alternative flow:** 1a. Selected slot was already booked → system asks the Patient to choose another available slot. 3a. Booking fails (e.g., connection/save error) → system keeps the slot open and shows an error message. |
| UC3 | Manage Appointment Request | Doctor | R3 | As a Doctor, I can accept or decline an appointment request. **Main flow:** 1. Doctor opens the list of pending appointment requests. 2. Doctor selects an appointment request. 3. Doctor accepts or declines the request. 4. System updates the appointment status (confirmed or declined). 5. System notifies the Patient of the decision. **Alternative flow:** 3a. Doctor leaves the request unhandled (closes the screen) → request stays "Pending" and can be managed later. |
| UC4 | Access Patient Medical Data | Authorized Staff | R5 | As Authorized Staff, I can access patient medical data only if I am authorized. **Main flow:** 1. Authorized Staff requests a patient's medical data. 2. System verifies the staff member's authorization. 3. System displays the patient medical data. **Alternative flow:** 2a. Requesting user is not authorized → system denies access and logs the attempt. |
| UC5 | Limit Upcoming Appointments | Patient | R4 | As a Patient, I can have at most **N** upcoming appointments at any given time. **Main flow:** 1. Patient books a new appointment (UC2, step 2). 2. System counts the Patient's upcoming appointments. 3. Count is less than **N**, so the system allows the booking to proceed. **Alternative flow:** 2a. Count is already **N** → system rejects the booking and tells the Patient to cancel an existing appointment first. |

### Notes on the Use Cases

- UC5 is the business rule from R4; it is triggered through UC2 but written as its own use case to keep exactly five.
- Non-functional requirements (R6 response time, R7 mobile screens) are not separate use cases — they constrain UC1–UC5.
