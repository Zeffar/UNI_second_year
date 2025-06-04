package ClinicApp.src;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class DatabaseConnection {
    private static final String URL = "jdbc:postgresql:
    private static final String USERNAME = "admin";
    private static final String PASSWORD = "admin";
    
    private Connection connection;
    
    public DatabaseConnection() throws SQLException {
        try {
            Class.forName("org.postgresql.Driver");
            this.connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
            System.out.println("Connected to PostgreSQL database successfully!");
        } catch (ClassNotFoundException e) {
            throw new SQLException("PostgreSQL JDBC driver not found", e);
        }
    }
    
    public void close() throws SQLException {
        if (connection != null && !connection.isClosed()) {
            connection.close();
            System.out.println("Database connection closed.");
        }
    }
    
    public List<MedicalSpecialty> getAllMedicalSpecialties() throws SQLException {
        List<MedicalSpecialty> specialties = new ArrayList<>();
        String sql = "SELECT id, name FROM medical_specialties ORDER BY name";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                specialties.add(new MedicalSpecialty(rs.getString("name")));
            }
        }
        return specialties;
    }
    
    public int getMedicalSpecialtyId(String specialtyName) throws SQLException {
        String sql = "SELECT id FROM medical_specialties WHERE name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, specialtyName);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        return -1;
    }
    
    public int insertAddress(Address address) throws SQLException {
        String sql = "INSERT INTO addresses (street, city, zip_code, country) VALUES (?, ?, ?, ?) RETURNING id";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, address.getStreet());
            stmt.setString(2, address.getCity());
            stmt.setString(3, address.getZipCode());
            stmt.setString(4, address.getCountry());
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        throw new SQLException("Failed to insert address");
    }
    
    public int insertContactInfo(ContactInfo contactInfo) throws SQLException {
        String sql = "INSERT INTO contact_info (phone_number, email) VALUES (?, ?) RETURNING id";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, contactInfo.getPhoneNumber());
            stmt.setString(2, contactInfo.getEmail());
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        throw new SQLException("Failed to insert contact info");
    }
    
    public int insertDoctor(Doctor doctor) throws SQLException {
        int addressId = insertAddress(doctor.getAddress());
        int contactInfoId = insertContactInfo(doctor.getContactInfo());
        int specialtyId = getMedicalSpecialtyId(doctor.getSpecialty().getName());
        
        String sql = "INSERT INTO doctors (first_name, last_name, contact_info_id, address_id, specialty_id) VALUES (?, ?, ?, ?, ?) RETURNING id";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, doctor.getFirstName());
            stmt.setString(2, doctor.getLastName());
            stmt.setInt(3, contactInfoId);
            stmt.setInt(4, addressId);
            stmt.setInt(5, specialtyId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        throw new SQLException("Failed to insert doctor");
    }
    
    public List<Doctor> getAllDoctors() throws SQLException {
        List<Doctor> doctors = new ArrayList<>();
        String sql = """
            SELECT d.id, d.first_name, d.last_name, 
                   ci.phone_number, ci.email,
                   a.street, a.city, a.zip_code, a.country,
                   ms.name as specialty_name
            FROM doctors d
            LEFT JOIN contact_info ci ON d.contact_info_id = ci.id
            LEFT JOIN addresses a ON d.address_id = a.id
            LEFT JOIN medical_specialties ms ON d.specialty_id = ms.id
            ORDER BY d.last_name, d.first_name
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                ContactInfo contactInfo = new ContactInfo(rs.getString("phone_number"), rs.getString("email"));
                Address address = new Address(rs.getString("street"), rs.getString("city"), 
                                            rs.getString("zip_code"), rs.getString("country"));
                MedicalSpecialty specialty = new MedicalSpecialty(rs.getString("specialty_name"));
                
                Doctor doctor = new Doctor(rs.getString("first_name"), rs.getString("last_name"), 
                                         contactInfo, address, specialty);
                doctors.add(doctor);
            }
        }
        return doctors;
    }
    
    public int insertPatient(Patient patient) throws SQLException {
        int addressId = insertAddress(patient.getAddress());
        int contactInfoId = insertContactInfo(patient.getContactInfo());
        
        String sql = "INSERT INTO patients (first_name, last_name, contact_info_id, address_id, date_of_birth) VALUES (?, ?, ?, ?, ?) RETURNING id";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, patient.getFirstName());
            stmt.setString(2, patient.getLastName());
            stmt.setInt(3, contactInfoId);
            stmt.setInt(4, addressId);
            stmt.setDate(5, Date.valueOf(patient.getDateOfBirth()));
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        throw new SQLException("Failed to insert patient");
    }
    
    public List<Patient> getAllPatients() throws SQLException {
        List<Patient> patients = new ArrayList<>();
        String sql = """
            SELECT p.id, p.first_name, p.last_name, p.date_of_birth,
                   ci.phone_number, ci.email,
                   a.street, a.city, a.zip_code, a.country
            FROM patients p
            LEFT JOIN contact_info ci ON p.contact_info_id = ci.id
            LEFT JOIN addresses a ON p.address_id = a.id
            ORDER BY p.last_name, p.first_name
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                ContactInfo contactInfo = new ContactInfo(rs.getString("phone_number"), rs.getString("email"));
                Address address = new Address(rs.getString("street"), rs.getString("city"), 
                                            rs.getString("zip_code"), rs.getString("country"));
                
                Patient patient = new Patient(rs.getString("first_name"), rs.getString("last_name"), 
                                            contactInfo, address, rs.getDate("date_of_birth").toLocalDate());
                patients.add(patient);
            }
        }
        return patients;
    }
    
    public int insertAppointment(int doctorId, int patientId, LocalDateTime dateTime, String reason) throws SQLException {
        String sql = "INSERT INTO appointments (doctor_id, patient_id, appointment_datetime, reason) VALUES (?, ?, ?, ?) RETURNING id";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, doctorId);
            stmt.setInt(2, patientId);
            stmt.setTimestamp(3, Timestamp.valueOf(dateTime));
            stmt.setString(4, reason);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("id");
                }
            }
        }
        throw new SQLException("Failed to insert appointment");
    }
    
    public List<String> getAllAppointments() throws SQLException {
        List<String> appointments = new ArrayList<>();
        String sql = """
            SELECT a.id, a.appointment_datetime, a.reason, a.status,
                   CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                   CONCAT(p.first_name, ' ', p.last_name) as patient_name
            FROM appointments a
            LEFT JOIN doctors d ON a.doctor_id = d.id
            LEFT JOIN patients p ON a.patient_id = p.id
            ORDER BY a.appointment_datetime
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                String appointment = String.format("ID: %d | %s | Doctor: %s | Patient: %s | Reason: %s | Status: %s",
                    rs.getInt("id"),
                    rs.getTimestamp("appointment_datetime").toString(),
                    rs.getString("doctor_name"),
                    rs.getString("patient_name"),
                    rs.getString("reason"),
                    rs.getString("status"));
                appointments.add(appointment);
            }
        }
        return appointments;
    }
    
    public boolean updateAppointmentStatus(int appointmentId, String status) throws SQLException {
        String sql = "UPDATE appointments SET status = ?::appointment_status WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, status);
            stmt.setInt(2, appointmentId);
            
            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        }
    }
    
    public List<String> getDoctorsList() throws SQLException {
        List<String> doctors = new ArrayList<>();
        String sql = "SELECT id, first_name, last_name FROM doctors ORDER BY last_name, first_name";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                doctors.add(String.format("ID: %d | %s %s", 
                    rs.getInt("id"), rs.getString("first_name"), rs.getString("last_name")));
            }
        }
        return doctors;
    }
    
    public List<String> getPatientsList() throws SQLException {
        List<String> patients = new ArrayList<>();
        String sql = "SELECT id, first_name, last_name FROM patients ORDER BY last_name, first_name";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                patients.add(String.format("ID: %d | %s %s", 
                    rs.getInt("id"), rs.getString("first_name"), rs.getString("last_name")));
            }
        }
        return patients;
    }
}
