# Clinic Appointments — Requirements

## Classification

Each requirement is classified as **Functional** or **Non-functional**.

| ID | Requirement | Type | Category |
|----|-------------|------|----------|
| R1 | A patient can view the days and times when a doctor is available. | Functional | Availability Viewing / Query |
| R2 | A patient can book an appointment during an available time slot. | Functional | Booking / Transaction |
| R3 | A doctor can accept or decline an appointment request. | Functional | Workflow / Business Decision |
| R4 | A patient can have at most **N** upcoming appointments at any given time. | Functional | Business Rule / Quantity Constraint |
| R5 | Patient medical data shall be accessible only to authorized staff. | Non-functional | Security / Access Control |
| R6 | Available appointment times shall be displayed within 2 seconds. | Non-functional | Performance / Response Time |
| R7 | The application shall be usable on mobile phone screens. | Non-functional | Usability / Portability |

---

## Design Decision — Value of N (R4)

Requirement R4 states "A patient can have at most **N** upcoming appointments at any given time." The team has chosen:

> **N = 3**

**Rationale:**
- Low enough to prevent a patient from hoarding doctors' time slots (each booked slot stays unavailable to other patients until confirmed or cancelled).
- High enough to cover a realistic patient scenario — for example a current visit plus a follow-up and one specialist appointment — without blocking legitimate bookings.
- The value is intentionally modeled as data (`AppointmentLimit.maxN`), not hard-coded logic, so the clinic can raise or lower it (e.g., **N = 5** for priority patients) without redesigning the system.

**Where it applies:**
- UC5 *Limit Upcoming Appointments* rejects any booking when the patient's upcoming appointment count is already 3.
- `Class-Diagram.md` — the `AppointmentLimit` class carries `maxN = 3`.
