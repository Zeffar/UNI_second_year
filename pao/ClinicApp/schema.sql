-- Database schema for Clinic Application
-- Tables: medical_specialties, addresses, contact_info, doctors, patients, appointments

-- Create Medical Specialties table
CREATE TABLE medical_specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Addresses table
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Create Contact Info table
CREATE TABLE contact_info (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

-- Create Doctors table
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    contact_info_id INTEGER REFERENCES contact_info(id),
    address_id INTEGER REFERENCES addresses(id),
    specialty_id INTEGER REFERENCES medical_specialties(id)
);

-- Create Patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    contact_info_id INTEGER REFERENCES contact_info(id),
    address_id INTEGER REFERENCES addresses(id),
    date_of_birth DATE NOT NULL
);

-- Create Appointment Status enum type
CREATE TYPE appointment_status AS ENUM ('SCHEDULED', 'COMPLETED', 'CANCELLED');

-- Create Appointments table
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id),
    patient_id INTEGER REFERENCES patients(id),
    appointment_datetime TIMESTAMP NOT NULL,
    reason TEXT,
    status appointment_status DEFAULT 'SCHEDULED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_datetime ON appointments(appointment_datetime);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_doctors_specialty ON doctors(specialty_id);

-- Insert initial medical specialties
INSERT INTO medical_specialties (name) VALUES 
    ('General Practice'),
    ('Cardiology'),
    ('Dermatology'),
    ('Neurology'),
    ('Orthopedics'),
    ('Pediatrics'),
    ('Psychiatry'),
    ('Radiology'),
    ('Surgery');

-- Display created tables
\dt

-- Display table structure
\d doctors
\d patients
\d appointments
