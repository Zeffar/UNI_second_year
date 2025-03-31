package ClinicApp.src;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;

public class Appointment implements Comparable<Appointment> {
    private static long idCounter = 0; 
    private long appointmentId;
    private Doctor doctor;
    private Patient patient;
    private LocalDateTime dateTime;
    private String reason;
    private AppointmentStatus status;

    public Appointment(Doctor doctor, Patient patient, LocalDateTime dateTime, String reason) {
        this.appointmentId = ++idCounter;
        if (doctor == null || patient == null || dateTime == null) {
            throw new IllegalArgumentException("Doctor, Patient, and DateTime cannot be null for an Appointment.");
        }
        this.doctor = doctor;
        this.patient = patient;
        this.dateTime = dateTime;
        this.reason = (reason != null) ? reason : "Routine Checkup";
        this.status = AppointmentStatus.SCHEDULED; 
    }

    public long getAppointmentId() {
        return appointmentId;
    }

    public Doctor getDoctor() {
        return doctor;
    }

    public Patient getPatient() {
        return patient;
    }

    public LocalDateTime getDateTime() {
        return dateTime;
    }

    public String getReason() {
        return reason;
    }

    public AppointmentStatus getStatus() {
        return status;
    }

    public void setStatus(AppointmentStatus status) {
        this.status = status;
    }

    public void setDateTime(LocalDateTime dateTime) {
        if (dateTime == null) {
            throw new IllegalArgumentException("DateTime cannot be null.");
        }
        this.dateTime = dateTime;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    @Override
    public String toString() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
        return "Appointment [ID: " + appointmentId +
                ", DateTime: " + dateTime.format(formatter) +
                ", Status: " + status +
                ", Doctor: " + doctor.getFullName() + " (ID: " + doctor.getPersonId() + ")" +
                ", Patient: " + patient.getFullName() + " (ID: " + patient.getPersonId() + ")" +
                ", Reason: '" + reason + '\'' +
                ']';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Appointment that = (Appointment) o;
        return appointmentId == that.appointmentId;
    }

    @Override
    public int hashCode() {
        return Objects.hash(appointmentId);
    }

    @Override
    public int compareTo(Appointment other) {
        int dateComparison = this.dateTime.compareTo(other.dateTime);
        if (dateComparison != 0) {
            return dateComparison;
        }
        return Long.compare(this.appointmentId, other.appointmentId);
    }
}