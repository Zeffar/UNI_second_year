# Clinic Application Database Schema

## Overview
This PostgreSQL database schema supports the Clinic Application with the following main entities:
- Medical Specialties
- Doctors
- Patients
- Appointments
- Addresses
- Contact Information

## Database Connection
- **Host**: Docker container named `postgres`
- **Database**: `pao`
- **Username**: `admin`
- **Password**: `admin`

## Tables Structure

### 1. medical_specialties
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(100) UNIQUE NOT NULL)

Pre-populated with: General Practice, Cardiology, Dermatology, Neurology, Orthopedics, Pediatrics, Psychiatry, Radiology, Surgery

### 2. addresses
- `id` (SERIAL PRIMARY KEY)
- `street` (VARCHAR(255) NOT NULL)
- `city` (VARCHAR(100) NOT NULL)
- `zip_code` (VARCHAR(20) NOT NULL)
- `country` (VARCHAR(100) NOT NULL)

### 3. contact_info
- `id` (SERIAL PRIMARY KEY)
- `phone_number` (VARCHAR(20))
- `email` (VARCHAR(100))

### 4. doctors
- `id` (SERIAL PRIMARY KEY)
- `first_name` (VARCHAR(100) NOT NULL)
- `last_name` (VARCHAR(100) NOT NULL)
- `contact_info_id` (INTEGER REFERENCES contact_info(id))
- `address_id` (INTEGER REFERENCES addresses(id))
- `specialty_id` (INTEGER REFERENCES medical_specialties(id))

### 5. patients
- `id` (SERIAL PRIMARY KEY)
- `first_name` (VARCHAR(100) NOT NULL)
- `last_name` (VARCHAR(100) NOT NULL)
- `contact_info_id` (INTEGER REFERENCES contact_info(id))
- `address_id` (INTEGER REFERENCES addresses(id))
- `date_of_birth` (DATE NOT NULL)

### 6. appointments
- `id` (SERIAL PRIMARY KEY)
- `doctor_id` (INTEGER REFERENCES doctors(id))
- `patient_id` (INTEGER REFERENCES patients(id))
- `appointment_datetime` (TIMESTAMP NOT NULL)
- `reason` (TEXT)
- `status` (appointment_status DEFAULT 'SCHEDULED')
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

## Indexes Created
- `idx_appointments_doctor_id` - for efficient doctor lookup
- `idx_appointments_patient_id` - for efficient patient lookup
- `idx_appointments_datetime` - for date-based queries
- `idx_appointments_status` - for status filtering
- `idx_doctors_specialty` - for specialty-based doctor searches

## Common Queries

### Connect to Database
```bash
docker exec -it postgres psql -U admin -d pao
```

### Find all doctors with their specialties
```sql
SELECT d.id, d.first_name, d.last_name, ms.name as specialty 
FROM doctors d 
LEFT JOIN medical_specialties ms ON d.specialty_id = ms.id;
```

### Find all appointments for a specific doctor
```sql
SELECT a.*, p.first_name as patient_first, p.last_name as patient_last
FROM appointments a
JOIN patients p ON a.patient_id = p.id
WHERE a.doctor_id = 1
ORDER BY a.appointment_datetime;
```

### Find appointments by date range
```sql
SELECT a.id, 
       CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
       a.appointment_datetime,
       a.status
FROM appointments a
JOIN doctors d ON a.doctor_id = d.id
JOIN patients p ON a.patient_id = p.id
WHERE a.appointment_datetime BETWEEN '2025-06-01' AND '2025-06-30'
ORDER BY a.appointment_datetime;
```

### Find doctors by specialty
```sql
SELECT d.*, ms.name as specialty_name
FROM doctors d
JOIN medical_specialties ms ON d.specialty_id = ms.id
WHERE ms.name = 'Cardiology';
```

### Update appointment status
```sql
UPDATE appointments 
SET status = 'COMPLETED' 
WHERE id = 1;
```

## Notes for Java Integration
- Use JDBC PostgreSQL driver: `org.postgresql:postgresql`
- Connection URL: `jdbc:postgresql://localhost:5432/pao` (if Docker port is mapped to 5432)
- The schema follows the structure of your Java classes but uses database-appropriate naming conventions
- IDs are auto-generated using SERIAL type (equivalent to AUTO_INCREMENT)
- Foreign key relationships maintain referential integrity
- The appointment_status ENUM matches your Java AppointmentStatus enum values
