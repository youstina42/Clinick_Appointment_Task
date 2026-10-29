class AppointmentLimit:
    """Rule: a patient may have at most N upcoming appointments."""

    N = 3


class TimeSlot:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.appointment = None

    def is_available(self):
        return self.appointment is None

    def __repr__(self):
        return f"TimeSlot({self.start!r}, {self.end!r})"


class Availability:
    def __init__(self, doctor):
        self.doctor = doctor
        self.time_slots = []

    def add_time_slot(self, time_slot):
        self.time_slots.append(time_slot)

    def getAvailableSlots(self, doctor):
        if doctor is not self.doctor:
            return []
        return [slot for slot in self.time_slots if slot.is_available()]

    def reserveSlot(self, appointment):
        slot = appointment.time_slot
        if appointment.doctor is not self.doctor:
            return False
        if slot is None or slot not in self.time_slots or not slot.is_available():
            return False
        slot.appointment = appointment
        return True


class MedicalRecord:
    def __init__(self, patient):
        self.patient = patient


class Patient:
    def __init__(self, name):
        self.name = name
        self.appointments = []
        self.medical_record = MedicalRecord(self)

    def bookAppointment(self):
        return AppointmentRequest(self)

    def countUpcomingAppointments(self):
        return sum(
            1 for appointment in self.appointments
            if appointment.status == "CONFIRMED"
        )


class Doctor:
    def __init__(self, name, accepts_appointments=True):
        self.name = name
        self.accepts_appointments = accepts_appointments
        self.availabilities = []

    def add_availability(self, availability):
        self.availabilities.append(availability)

    def confirmAppointment(self, appointment):
        return self.accepts_appointments


class AppointmentRequest:
    def __init__(self, patient, doctor=None):
        self.patient = patient
        self.doctor = doctor
        self.status = "PENDING"
        self.appointment = None


class Appointment:
    def __init__(self, patient, doctor, availability, time_slot=None, request=None):
        self.patient = patient
        self.doctor = doctor
        self.availability = availability
        self.time_slot = time_slot
        self.status = "PENDING"
        self.request = request if request is not None else AppointmentRequest(patient, doctor)
        self.request.doctor = doctor
        self.request.appointment = self

    def submit(self):
        if self.status != "PENDING":
            return self.status

        available_slots = self.availability.getAvailableSlots(self.doctor)
        if not available_slots:
            return self._finish("NO_SLOT_AVAILABLE")

        if self.time_slot not in available_slots:
            return self._finish("SLOT_UNAVAILABLE")

        if self.patient.countUpcomingAppointments() >= AppointmentLimit.N:
            return self._finish("LIMIT_REACHED")

        if not self.doctor.confirmAppointment(self):
            return self._finish("DECLINED")

        if not self.availability.reserveSlot(self):
            return self._finish("SLOT_UNAVAILABLE")

        self.patient.appointments.append(self)
        return self._finish("CONFIRMED")

    def _finish(self, status):
        self.status = status
        self.request.status = status
        return status


class Payment:
    def __init__(self, amount=0.0):
        self.amount = amount


class GPS_Location:
    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = latitude
        self.longitude = longitude


class Notification:
    def __init__(self, message=""):
        self.message = message


class Clinic:
    def __init__(self, name=""):
        self.name = name


def main():
    doctor = Doctor("Dr. Rivera", accepts_appointments=True)
    availability = Availability(doctor)
    doctor.add_availability(availability)

    first_slot = TimeSlot("2026-11-02 09:00", "2026-11-02 09:30")
    second_slot = TimeSlot("2026-11-02 09:30", "2026-11-02 10:00")
    availability.add_time_slot(first_slot)
    availability.add_time_slot(second_slot)

    # Successful booking.
    alice = Patient("Alice")
    request = alice.bookAppointment()
    appointment = Appointment(alice, doctor, availability, first_slot, request)
    print("Successful booking status:", appointment.submit())

    # Rejected booking because Bob already has N upcoming appointments.
    bob = Patient("Bob")
    for index in range(AppointmentLimit.N):
        existing = Appointment(
            bob,
            doctor,
            availability,
            TimeSlot(f"2026-11-03 {9 + index}:00", f"2026-11-03 {9 + index}:30"),
        )
        existing.status = "CONFIRMED"
        bob.appointments.append(existing)

    rejected_request = bob.bookAppointment()
    rejected = Appointment(bob, doctor, availability, second_slot, rejected_request)
    print("Rejected booking status:", rejected.submit())


if __name__ == "__main__":
    main()
