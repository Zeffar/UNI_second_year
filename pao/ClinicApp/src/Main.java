package ClinicApp.src;

import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Scanner;

public class Main {
    private static DatabaseConnection dbConnection;
    private static Scanner scanner = new Scanner(System.in);
    private static AuditService auditService;

    public static void main(String[] args) {
        try {
            dbConnection = new DatabaseConnection();
            auditService = AuditService.getInstance();
            auditService.logAction("APPLICATION_STARTED");
            
            System.out.println("=== Medical Cabinet Appointment System ===");
            System.out.println("Connected to database successfully!");
            
            boolean running = true;
            while (running) {
                showMainMenu();
                int choice = getIntInput("Enter your choice: ");
                
                switch (choice) {
                    case 1 -> {
                        auditService.logAction("ACCESSED_DOCTOR_OPERATIONS");
                        handleDoctorOperations();
                    }
                    case 2 -> {
                        auditService.logAction("ACCESSED_PATIENT_OPERATIONS");
                        handlePatientOperations();
                    }
                    case 3 -> {
                        auditService.logAction("ACCESSED_APPOINTMENT_OPERATIONS");
                        handleAppointmentOperations();
                    }
                    case 4 -> {
                        auditService.logAction("VIEWED_ALL_DATA");
                        showAllData();
                    }
                    case 5 -> {
                        auditService.logAction("VIEWED_AUDIT_LOG");
                        viewAuditLog();
                    }
                    case 6 -> {
                        auditService.logAction("APPLICATION_EXITED");
                        System.out.println("Exiting application...");
                        running = false;
                    }
                    default -> System.out.println("Invalid choice. Please try again.");
                }
                
                if (running) {
                    System.out.println("\nPress Enter to continue...");
                    scanner.nextLine();
                }
            }
            
        } catch (SQLException e) {
            System.err.println("Database connection error: " + e.getMessage());
            System.err.println("Make sure PostgreSQL is running and the database 'pao' exists.");
        } finally {
            try {
                if (dbConnection != null) {
                    dbConnection.close();
                }
                scanner.close();
            } catch (SQLException e) {
                System.err.println("Error closing database connection: " + e.getMessage());
            }
        }
    }
    
    private static void showMainMenu() {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("           MAIN MENU");
        System.out.println("=".repeat(50));
        System.out.println("1. Doctor Operations");
        System.out.println("2. Patient Operations");
        System.out.println("3. Appointment Operations");
        System.out.println("4. View All Data");
        System.out.println("5. View Audit Log");
        System.out.println("6. Exit");
        System.out.println("=".repeat(50));
    }
    
    private static void handleDoctorOperations() {
        System.out.println("\n--- Doctor Operations ---");
        System.out.println("1. Add New Doctor");
        System.out.println("2. View All Doctors");
        System.out.println("3. View Medical Specialties");
        
        int choice = getIntInput("Enter choice: ");
        
        try {
            switch (choice) {
                case 1 -> {
                    auditService.logAction("ADD_NEW_DOCTOR_INITIATED");
                    try {
                        addNewDoctor();
                    } catch (SQLException e) {
                        auditService.logActionWithDetails("DOCTOR_ADDITION_FAILED_DATABASE_ERROR", 
                            "Error: " + e.getMessage());
                        throw e;
                    }
                }
                case 2 -> {
                    auditService.logAction("VIEW_ALL_DOCTORS");
                    viewAllDoctors();
                }
                case 3 -> {
                    auditService.logAction("VIEW_MEDICAL_SPECIALTIES");
                    viewMedicalSpecialties();
                }
                default -> System.out.println("Invalid choice.");
            }
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
    
    private static void handlePatientOperations() {
        System.out.println("\n--- Patient Operations ---");
        System.out.println("1. Add New Patient");
        System.out.println("2. View All Patients");
        
        int choice = getIntInput("Enter choice: ");
        
        try {
            switch (choice) {
                case 1 -> {
                    auditService.logAction("ADD_NEW_PATIENT_INITIATED");
                    try {
                        addNewPatient();
                    } catch (SQLException e) {
                        auditService.logActionWithDetails("PATIENT_ADDITION_FAILED_DATABASE_ERROR", 
                            "Error: " + e.getMessage());
                        throw e;
                    }
                }
                case 2 -> {
                    auditService.logAction("VIEW_ALL_PATIENTS");
                    viewAllPatients();
                }
                default -> System.out.println("Invalid choice.");
            }
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
    
    private static void handleAppointmentOperations() {
        System.out.println("\n--- Appointment Operations ---");
        System.out.println("1. Schedule New Appointment");
        System.out.println("2. View All Appointments");
        System.out.println("3. Update Appointment Status");
        
        int choice = getIntInput("Enter choice: ");
        
        try {
            switch (choice) {
                case 1 -> {
                    auditService.logAction("SCHEDULE_NEW_APPOINTMENT_INITIATED");
                    try {
                        scheduleNewAppointment();
                    } catch (SQLException e) {
                        auditService.logActionWithDetails("APPOINTMENT_SCHEDULING_FAILED_DATABASE_ERROR", 
                            "Error: " + e.getMessage());
                        throw e;
                    }
                }
                case 2 -> {
                    auditService.logAction("VIEW_ALL_APPOINTMENTS");
                    viewAllAppointments();
                }
                case 3 -> {
                    auditService.logAction("UPDATE_APPOINTMENT_STATUS_INITIATED");
                    try {
                        updateAppointmentStatus();
                    } catch (SQLException e) {
                        auditService.logActionWithDetails("APPOINTMENT_STATUS_UPDATE_FAILED_DATABASE_ERROR", 
                            "Error: " + e.getMessage());
                        throw e;
                    }
                }
                default -> System.out.println("Invalid choice.");
            }
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
    
    private static void addNewDoctor() throws SQLException {
        System.out.println("\n--- Adding New Doctor ---");
        
        System.out.print("First Name: ");
        String firstName = scanner.nextLine().trim();
        
        System.out.print("Last Name: ");
        String lastName = scanner.nextLine().trim();
        
        System.out.print("Phone Number: ");
        String phone = scanner.nextLine().trim();
        
        System.out.print("Email: ");
        String email = scanner.nextLine().trim();
        
        System.out.print("Street Address: ");
        String street = scanner.nextLine().trim();
        
        System.out.print("City: ");
        String city = scanner.nextLine().trim();
        
        System.out.print("Zip Code: ");
        String zipCode = scanner.nextLine().trim();
        
        System.out.print("Country: ");
        String country = scanner.nextLine().trim();
        
        System.out.println("\nAvailable Medical Specialties:");
        List<MedicalSpecialty> specialties = dbConnection.getAllMedicalSpecialties();
        for (int i = 0; i < specialties.size(); i++) {
            System.out.println((i + 1) + ". " + specialties.get(i).getName());
        }
        
        int specialtyChoice = getIntInput("Select specialty (number): ") - 1;
        if (specialtyChoice < 0 || specialtyChoice >= specialties.size()) {
            System.out.println("Invalid specialty choice.");
            auditService.logAction("DOCTOR_ADDITION_FAILED_INVALID_SPECIALTY");
            return;
        }
        
        ContactInfo contactInfo = new ContactInfo(phone, email);
        Address address = new Address(street, city, zipCode, country);
        MedicalSpecialty specialty = specialties.get(specialtyChoice);
        Doctor doctor = new Doctor(firstName, lastName, contactInfo, address, specialty);
        
        int doctorId = dbConnection.insertDoctor(doctor);
        System.out.println("Doctor added successfully with ID: " + doctorId);
        
        auditService.logActionWithDetails("DOCTOR_ADDED_TO_DATABASE", 
            String.format("Doctor: %s %s, ID: %d, Specialty: %s", 
                firstName, lastName, doctorId, specialty.getName()));
    }
    
    private static void addNewPatient() throws SQLException {
        System.out.println("\n--- Adding New Patient ---");
        
        System.out.print("First Name: ");
        String firstName = scanner.nextLine().trim();
        
        System.out.print("Last Name: ");
        String lastName = scanner.nextLine().trim();
        
        System.out.print("Phone Number: ");
        String phone = scanner.nextLine().trim();
        
        System.out.print("Email: ");
        String email = scanner.nextLine().trim();
        
        System.out.print("Street Address: ");
        String street = scanner.nextLine().trim();
        
        System.out.print("City: ");
        String city = scanner.nextLine().trim();
        
        System.out.print("Zip Code: ");
        String zipCode = scanner.nextLine().trim();
        
        System.out.print("Country: ");
        String country = scanner.nextLine().trim();
        
        LocalDate dateOfBirth = null;
        while (dateOfBirth == null) {
            System.out.print("Date of Birth (YYYY-MM-DD): ");
            String dobInput = scanner.nextLine().trim();
            try {
                dateOfBirth = LocalDate.parse(dobInput);
            } catch (DateTimeParseException e) {
                System.out.println("Invalid date format. Please use YYYY-MM-DD format.");
            }
        }
        
        ContactInfo contactInfo = new ContactInfo(phone, email);
        Address address = new Address(street, city, zipCode, country);
        Patient patient = new Patient(firstName, lastName, contactInfo, address, dateOfBirth);
        
        int patientId = dbConnection.insertPatient(patient);
        System.out.println("Patient added successfully with ID: " + patientId);
        
        auditService.logActionWithDetails("PATIENT_ADDED_TO_DATABASE", 
            String.format("Patient: %s %s, ID: %d, DOB: %s", 
                firstName, lastName, patientId, dateOfBirth.toString()));
    }
    
    private static void scheduleNewAppointment() throws SQLException {
        System.out.println("\n--- Scheduling New Appointment ---");
        
        System.out.println("\nAvailable Doctors:");
        List<String> doctors = dbConnection.getDoctorsList();
        for (String doctor : doctors) {
            System.out.println(doctor);
        }
        
        int doctorId = getIntInput("Enter Doctor ID: ");
        
        System.out.println("\nAvailable Patients:");
        List<String> patients = dbConnection.getPatientsList();
        for (String patient : patients) {
            System.out.println(patient);
        }
        
        int patientId = getIntInput("Enter Patient ID: ");
        
        LocalDateTime appointmentDateTime = null;
        while (appointmentDateTime == null) {
            System.out.print("Appointment Date and Time (YYYY-MM-DD HH:mm): ");
            String dateTimeInput = scanner.nextLine().trim();
            try {
                appointmentDateTime = LocalDateTime.parse(dateTimeInput, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
            } catch (DateTimeParseException e) {
                System.out.println("Invalid date/time format. Please use YYYY-MM-DD HH:mm format.");
            }
        }
        
        System.out.print("Reason for appointment: ");
        String reason = scanner.nextLine().trim();
        
        int appointmentId = dbConnection.insertAppointment(doctorId, patientId, appointmentDateTime, reason);
        System.out.println("Appointment scheduled successfully with ID: " + appointmentId);
        
        auditService.logActionWithDetails("APPOINTMENT_SCHEDULED_IN_DATABASE", 
            String.format("Appointment ID: %d, Doctor ID: %d, Patient ID: %d, DateTime: %s, Reason: %s", 
                appointmentId, doctorId, patientId, appointmentDateTime.toString(), reason));
    }
    
    private static void viewAllDoctors() throws SQLException {
        System.out.println("\n--- All Doctors ---");
        List<Doctor> doctors = dbConnection.getAllDoctors();
        if (doctors.isEmpty()) {
            System.out.println("No doctors found in the database.");
        } else {
            for (Doctor doctor : doctors) {
                System.out.println(doctor);
            }
        }
    }
    
    private static void viewAllPatients() throws SQLException {
        System.out.println("\n--- All Patients ---");
        List<Patient> patients = dbConnection.getAllPatients();
        if (patients.isEmpty()) {
            System.out.println("No patients found in the database.");
        } else {
            for (Patient patient : patients) {
                System.out.println(patient);
            }
        }
    }
    
    private static void viewAllAppointments() throws SQLException {
        System.out.println("\n--- All Appointments ---");
        List<String> appointments = dbConnection.getAllAppointments();
        if (appointments.isEmpty()) {
            System.out.println("No appointments found in the database.");
        } else {
            for (String appointment : appointments) {
                System.out.println(appointment);
            }
        }
    }
    
    private static void viewMedicalSpecialties() throws SQLException {
        System.out.println("\n--- Medical Specialties ---");
        List<MedicalSpecialty> specialties = dbConnection.getAllMedicalSpecialties();
        for (int i = 0; i < specialties.size(); i++) {
            System.out.println((i + 1) + ". " + specialties.get(i).getName());
        }
    }
    
    private static void updateAppointmentStatus() throws SQLException {
        System.out.println("\n--- Update Appointment Status ---");
        
        viewAllAppointments();
        
        int appointmentId = getIntInput("\nEnter Appointment ID to update: ");
        
        System.out.println("Status options:");
        System.out.println("1. SCHEDULED");
        System.out.println("2. COMPLETED");
        System.out.println("3. CANCELLED");
        
        int statusChoice = getIntInput("Select new status (number): ");
        String status;
        
        switch (statusChoice) {
            case 1 -> status = "SCHEDULED";
            case 2 -> status = "COMPLETED";
            case 3 -> status = "CANCELLED";
            default -> {
                System.out.println("Invalid status choice.");
                return;
            }
        }
        
        boolean updated = dbConnection.updateAppointmentStatus(appointmentId, status);
        if (updated) {
            System.out.println("Appointment status updated successfully to: " + status);
            
            auditService.logActionWithDetails("APPOINTMENT_STATUS_UPDATED", 
                String.format("Appointment ID: %d, New Status: %s", appointmentId, status));
        } else {
            System.out.println("Failed to update appointment. Please check the appointment ID.");
            auditService.logActionWithDetails("APPOINTMENT_STATUS_UPDATE_FAILED", 
                String.format("Appointment ID: %d, Attempted Status: %s", appointmentId, status));
        }
    }
    
    private static void showAllData() {
        try {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("                    ALL DATA OVERVIEW");
            System.out.println("=".repeat(60));
            
            viewAllDoctors();
            System.out.println();
            viewAllPatients();
            System.out.println();
            viewAllAppointments();
            
        } catch (SQLException e) {
            System.err.println("Error retrieving data: " + e.getMessage());
        }
    }
    
    private static void viewAuditLog() {
        System.out.println("\n--- Audit Log Operations ---");
        System.out.println("1. View Recent Audit Entries (Last 10)");
        System.out.println("2. View Recent Audit Entries (Last 20)");
        System.out.println("3. Clear Audit Log");
        
        int choice = getIntInput("Enter choice: ");
        
        switch (choice) {
            case 1 -> {
                auditService.displayRecentAuditEntries(10);
                auditService.logAction("VIEWED_RECENT_AUDIT_10");
            }
            case 2 -> {
                auditService.displayRecentAuditEntries(20);
                auditService.logAction("VIEWED_RECENT_AUDIT_20");
            }
            case 3 -> {
                System.out.print("Are you sure you want to clear the audit log? (y/N): ");
                String confirmation = scanner.nextLine().trim().toLowerCase();
                if (confirmation.equals("y") || confirmation.equals("yes")) {
                    auditService.clearAuditLog();
                    auditService.logAction("AUDIT_LOG_CLEARED");
                } else {
                    System.out.println("Audit log clear cancelled.");
                }
            }
            default -> System.out.println("Invalid choice.");
        }
    }
    
    private static int getIntInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                String input = scanner.nextLine().trim();
                return Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }
        }
    }
}