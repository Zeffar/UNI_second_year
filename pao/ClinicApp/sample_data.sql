-- Sample data insertion for testing the clinic database

-- Insert sample addresses
INSERT INTO addresses (street, city, zip_code, country) VALUES 
    ('221B Baker St', 'Princeton', '08540', 'USA'),
    ('10 Downing St', 'Princeton', '08540', 'USA'),
    ('1 Hospital Plz', 'Princeton', '08540', 'USA'),
    ('123 Main St', 'Anytown', '12345', 'USA'),
    ('456 Oak Ave', 'Otherville', '67890', 'USA');

-- Insert sample contact info
INSERT INTO contact_info (phone_number, email) VALUES 
    ('555-1234', 'house@clinic.com'),
    ('555-5678', 'wilson@clinic.com'),
    ('555-9999', 'cuddy@clinic.com'),
    ('111-2222', 'john.d@mail.com'),
    ('333-4444', 'jane.s@mail.com');

-- Insert sample doctors
INSERT INTO doctors (first_name, last_name, contact_info_id, address_id, specialty_id) VALUES 
    ('Gregory', 'House', 1, 1, 1),  -- General Practice
    ('James', 'Wilson', 2, 2, 2),   -- Cardiology
    ('Lisa', 'Cuddy', 3, 3, 3);     -- Dermatology

-- Insert sample patients
INSERT INTO patients (first_name, last_name, contact_info_id, address_id, date_of_birth) VALUES 
    ('John', 'Doe', 4, 4, '1985-05-15'),
    ('Jane', 'Smith', 5, 5, '1992-08-20');

-- Insert sample appointments
INSERT INTO appointments (doctor_id, patient_id, appointment_datetime, reason, status) VALUES 
    (2, 1, '2025-06-07 10:00:00', 'Heart checkup', 'SCHEDULED'),
    (1, 2, '2025-06-07 11:00:00', 'General consultation', 'SCHEDULED'),
    (3, 1, '2025-06-08 09:30:00', 'Skin rash', 'SCHEDULED');

-- Verify the data
SELECT 'Doctors:' as table_name;
SELECT d.id, d.first_name, d.last_name, ms.name as specialty, ci.email, ci.phone_number 
FROM doctors d 
LEFT JOIN medical_specialties ms ON d.specialty_id = ms.id
LEFT JOIN contact_info ci ON d.contact_info_id = ci.id;

SELECT 'Patients:' as table_name;
SELECT p.id, p.first_name, p.last_name, p.date_of_birth, ci.email, ci.phone_number 
FROM patients p 
LEFT JOIN contact_info ci ON p.contact_info_id = ci.id;

SELECT 'Appointments:' as table_name;
SELECT a.id, 
       CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
       a.appointment_datetime,
       a.reason,
       a.status
FROM appointments a
LEFT JOIN doctors d ON a.doctor_id = d.id
LEFT JOIN patients p ON a.patient_id = p.id
ORDER BY a.appointment_datetime;
