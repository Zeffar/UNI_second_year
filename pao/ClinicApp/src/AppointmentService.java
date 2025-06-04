package ClinicApp.src;
import java.time.LocalDateTime;
import java.util.*;
import java.time.LocalDate;
import java.util.stream.Collectors;

public class AppointmentService {

    private List<Doctor> doctors;
    private List<Patient> patients;

    private SortedSet<Appointment> appointments; 
    private Map<Long, Doctor> doctorById;
    private Map<Long, Patient> patientById;
    private Map<Long, Appointment> appointmentById;
    public AppointmentService() {
        this.doctors = new ArrayList<>();
        this.patients = new ArrayList<>();
        this.appointments = new TreeSet<>(); 

        this.doctorById = new HashMap<>();
        this.patientById = new HashMap<>();
        this.appointmentById = new HashMap<>();
    }

    public Doctor addDoctor(String firstName, String lastName, ContactInfo contactInfo, Address address, MedicalSpecialty specialty) {
        Doctor newDoctor = new Doctor(firstName, lastName, contactInfo, address, specialty);
        this.doctors.add(newDoctor);
        this.doctorById.put(newDoctor.getPersonId(), newDoctor);
        System.out.println("Doctor added: " + newDoctor.getFullName());
        return newDoctor;
    }

    public List<Doctor> getAllDoctors() {
        return Collections.unmodifiableList(this.doctors); 
    }

    public Doctor findDoctorById(long id) {
        return this.doctorById.get(id);
    }

     public List<Doctor> findDoctorsBySpecialty(MedicalSpecialty specialty) {
        return this.doctors.stream()
                .filter(doctor -> doctor.getSpecialty().equals(specialty))
                .collect(Collectors.toList());
    }
    public Patient addPatient(String firstName, String lastName, ContactInfo contactInfo, Address address, LocalDate dateOfBirth) {
        Patient newPatient = new Patient(firstName, lastName, contactInfo, address, dateOfBirth);
        this.patients.add(newPatient);
        this.patientById.put(newPatient.getPersonId(), newPatient);
        System.out.println("Patient added: " + newPatient.getFullName());
        return newPatient;
    }

    public List<Patient> getAllPatients() {
        return Collections.unmodifiableList(this.patients); 
    }

    public Patient findPatientById(long id) {
         return this.patientById.get(id);
    }

    public Appointment scheduleAppointment(long doctorId, long patientId, LocalDateTime dateTime, String reason) {
        Doctor doctor = findDoctorById(doctorId);
        Patient patient = findPatientById(patientId);

        if (doctor == null) {
            System.err.println("Error scheduling: Doctor with ID " + doctorId + " not found.");
            return null;
        }
        if (patient == null) {
            System.err.println("Error scheduling: Patient with ID " + patientId + " not found.");
            return null;
        }
        if (dateTime == null || dateTime.isBefore(LocalDateTime.now())) {
             System.err.println("Error scheduling: Appointment date/time must be in the future.");
            return null;
        }

        boolean conflict = appointments.stream()
                .anyMatch(app -> app.getDoctor().equals(doctor) && app.getDateTime().equals(dateTime) && app.getStatus() == AppointmentStatus.SCHEDULED);
        if (conflict) {
             System.err.println("Error scheduling: Doctor " + doctor.getFullName() + " already has an appointment at " + dateTime);
            return null;
        }
        Appointment newAppointment = new Appointment(doctor, patient, dateTime, reason);
        this.appointments.add(newAppointment); 
        this.appointmentById.put(newAppointment.getAppointmentId(), newAppointment);
        System.out.println("Appointment scheduled: " + newAppointment);
        return newAppointment;
    }

    public Appointment findAppointmentById(long id) {
        return this.appointmentById.get(id);
    }
    public boolean cancelAppointment(long appointmentId) {
        Appointment appointment = findAppointmentById(appointmentId);
        if (appointment != null && appointment.getStatus() == AppointmentStatus.SCHEDULED) {
            appointment.setStatus(AppointmentStatus.CANCELLED);
            System.out.println("Appointment cancelled: ID " + appointmentId);
            return true;
        } else if (appointment != null) {
             System.err.println("Error cancelling: Appointment ID " + appointmentId + " cannot be cancelled (Status: " + appointment.getStatus() + ")");
             return false;
        } else {
            System.err.println("Error cancelling: Appointment ID " + appointmentId + " not found.");
            return false;
        }
    }

     public boolean completeAppointment(long appointmentId) {
        Appointment appointment = findAppointmentById(appointmentId);
        if (appointment != null && appointment.getStatus() == AppointmentStatus.SCHEDULED) {
            appointment.setStatus(AppointmentStatus.COMPLETED);
             System.out.println("Appointment marked as completed: ID " + appointmentId);
            return true;
        } else if (appointment != null) {
             System.err.println("Error completing: Appointment ID " + appointmentId + " cannot be completed (Status: " + appointment.getStatus() + ")");
             return false;
        } else {
            System.err.println("Error completing: Appointment ID " + appointmentId + " not found.");
            return false;
        }
    }

    public SortedSet<Appointment> getAllAppointmentsSorted() {
        return Collections.unmodifiableSortedSet(this.appointments);
    }

    public List<Appointment> getAppointmentsForDoctor(long doctorId) {
        Doctor doctor = findDoctorById(doctorId);
        if (doctor == null) {
            return Collections.emptyList(); 
        }
        return this.appointments.stream()
                .filter(app -> app.getDoctor().equals(doctor))
                .collect(Collectors.toList());
    }

     public List<Appointment> getAppointmentsForPatient(long patientId) {
        Patient patient = findPatientById(patientId);
         if (patient == null) {
            return Collections.emptyList(); 
        }
        return this.appointments.stream()
                .filter(app -> app.getPatient().equals(patient))
                .collect(Collectors.toList());
    }
}
