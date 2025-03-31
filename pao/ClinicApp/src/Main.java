package ClinicApp.src;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        System.out.println("--- Medical Cabinet Appointment System ---");

        AppointmentService service = new AppointmentService();

        MedicalSpecialty cardiology = new MedicalSpecialty("Cardiology");
        MedicalSpecialty dermatology = new MedicalSpecialty("Dermatology");
        MedicalSpecialty general = new MedicalSpecialty("General Practice");

        // 1. Add Doctors
        System.out.println("\n--- Adding Doctors ---");
        Doctor drHouse = service.addDoctor("Gregory", "House", new ContactInfo("555-1234", "house@clinic.com"),
                new Address("221B Baker St", "Princeton", "08540", "USA"), general);
        Doctor drWilson = service.addDoctor("James", "Wilson", new ContactInfo("555-5678", "wilson@clinic.com"),
                new Address("10 Downing St", "Princeton", "08540", "USA"), cardiology);
        Doctor drCuddy = service.addDoctor("Lisa", "Cuddy", new ContactInfo("555-9999", "cuddy@clinic.com"),
                new Address("1 Hospital Plz", "Princeton", "08540", "USA"), dermatology); // Changed specialty

        // 6. List all Doctors
        System.out.println("\n--- All Doctors ---");
        service.getAllDoctors().forEach(System.out::println);

        // 11. Find Doctors by Specialty
        System.out.println("\n--- Doctors with Specialty: " + cardiology.getName() + " ---");
        List<Doctor> cardiologists = service.findDoctorsBySpecialty(cardiology);
        cardiologists.forEach(System.out::println);

        // 2. Add Patients
        System.out.println("\n--- Adding Patients ---");
        Patient patientJohn = service.addPatient("John", "Doe", new ContactInfo("111-2222", "john.d@mail.com"),
                new Address("123 Main St", "Anytown", "12345", "USA"), LocalDate.of(1985, 5, 15));
        Patient patientJane = service.addPatient("Jane", "Smith", new ContactInfo("333-4444", "jane.s@mail.com"),
                new Address("456 Oak Ave", "Otherville", "67890", "USA"), LocalDate.of(1992, 8, 20));

        // 7. List all Patients
        System.out.println("\n--- All Patients ---");
        service.getAllPatients().forEach(System.out::println);

        // 12. Find Patient by ID
        System.out.println("\n--- Finding Patient ID: " + patientJohn.getPersonId() + " ---");
        Patient foundPatient = service.findPatientById(patientJohn.getPersonId());
        System.out.println("Found: " + foundPatient);

        // 3. Schedule Appointments
        System.out.println("\n--- Scheduling Appointments ---");
        LocalDateTime time1 = LocalDateTime.now().plusDays(3).withHour(10).withMinute(0).withSecond(0).withNano(0);
        LocalDateTime time2 = LocalDateTime.now().plusDays(3).withHour(11).withMinute(0).withSecond(0).withNano(0);
        LocalDateTime time3 = LocalDateTime.now().plusDays(4).withHour(9).withMinute(30).withSecond(0).withNano(0);
        LocalDateTime time4 = LocalDateTime.now().plusDays(3).withHour(10).withMinute(0).withSecond(0).withNano(0); // Conflict
                                                                                                                    // time
                                                                                                                    // with
                                                                                                                    // appt1

        Appointment appt1 = service.scheduleAppointment(drWilson.getPersonId(), patientJohn.getPersonId(), time1,
                "Heart checkup");
        Appointment appt2 = service.scheduleAppointment(drHouse.getPersonId(), patientJane.getPersonId(), time2,
                "General consultation");
        Appointment appt3 = service.scheduleAppointment(drCuddy.getPersonId(), patientJohn.getPersonId(), time3,
                "Skin rash");
        service.scheduleAppointment(drWilson.getPersonId(), patientJane.getPersonId(), time4, "Follow-up"); // Should
                                                                                                            // fail
                                                                                                            // (conflict)
        service.scheduleAppointment(999, patientJane.getPersonId(), time2.plusHours(1), "Checkup"); // Should fail (bad
                                                                                                    // doctor ID)

        // 8. List all Appointments (Sorted)
        System.out.println("\n--- All Appointments (Sorted by Date) ---");
        service.getAllAppointmentsSorted().forEach(System.out::println);

        // 9. List Appointments for a specific Doctor
        System.out.println("\n--- Appointments for Dr. " + drWilson.getLastName() + " ---");
        service.getAppointmentsForDoctor(drWilson.getPersonId()).forEach(System.out::println);

        // 10. List Appointments for a specific Patient
        System.out.println("\n--- Appointments for Patient " + patientJohn.getLastName() + " ---");
        service.getAppointmentsForPatient(patientJohn.getPersonId()).forEach(System.out::println);

        // 4. Cancel an Appointment
        System.out.println(
                "\n--- Cancelling Appointment ID: " + (appt2 != null ? appt2.getAppointmentId() : "N/A") + " ---");
        if (appt2 != null) {
            service.cancelAppointment(appt2.getAppointmentId());
        }

        // 5. Complete an Appointment
        System.out.println(
                "\n--- Completing Appointment ID: " + (appt1 != null ? appt1.getAppointmentId() : "N/A") + " ---");
        if (appt1 != null) {
            service.completeAppointment(appt1.getAppointmentId());
        }
        // Try cancelling already completed appointment
        if (appt1 != null) {
            service.cancelAppointment(appt1.getAppointmentId()); // Should fail
        }

        // 14. Get details of a specific Appointment by ID
        System.out.println(
                "\n--- Details for Appointment ID: " + (appt3 != null ? appt3.getAppointmentId() : "N/A") + " ---");
        if (appt3 != null) {
            Appointment specificAppt = service.findAppointmentById(appt3.getAppointmentId());
            System.out.println("Found: " + specificAppt);
        }

        System.out.println("\n--- Final List of Appointments (Sorted) ---");
        service.getAllAppointmentsSorted().forEach(System.out::println);

        System.out.println("\n--- System Demo Complete ---");
    }
}