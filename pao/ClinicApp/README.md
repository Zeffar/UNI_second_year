# Medical Cabinet Appointment System

A comprehensive clinic management system with a command-line interface that connects to a PostgreSQL database.

## Features

- **Doctor Management**: Add and view doctors with their specialties, contact information, and addresses
- **Patient Management**: Add and view patients with their personal information and medical history
- **Appointment Scheduling**: Schedule, view, and update appointment status
- **Database Integration**: Full PostgreSQL database connectivity with proper data persistence
- **Interactive CLI**: User-friendly command-line interface for all operations
- **Audit Service**: Comprehensive logging of all user actions and database operations to CSV file

## Prerequisites

1. **Java Development Kit (JDK)** - Version 8 or higher
2. **Docker** - For running PostgreSQL database
3. **PostgreSQL Docker Container** - Already configured with database "pao"

## Database Setup

The application uses a PostgreSQL database running in a Docker container:
- **Container Name**: postgres
- **Database**: pao
- **Username**: admin
- **Password**: admin
- **Port**: 5432

Make sure your PostgreSQL container is running:
```bash
docker ps
```

## Installation and Setup

1. **Download Dependencies**:
   ```bash
   ./lib/download_dependencies.sh
   ```

2. **Compile the Application**:
   ```bash
   javac -cp "lib/postgresql-42.7.1.jar:src" src/*.java -d bin/
   ```

3. **Run the Application**:
   ```bash
   ./run.sh
   ```
   
   Or manually:
   ```bash
   java -cp "lib/postgresql-42.7.1.jar:bin" ClinicApp.src.Main
   ```

## Usage

The application provides an interactive CLI with the following main options:

### 1. Doctor Operations
- Add new doctors with contact info, address, and medical specialty
- View all doctors in the system
- View available medical specialties

### 2. Patient Operations
- Add new patients with personal information and date of birth
- View all patients in the system

### 3. Appointment Operations
- Schedule new appointments between doctors and patients
- View all scheduled appointments
- Update appointment status (SCHEDULED, COMPLETED, CANCELLED)

### 4. View All Data
- Display comprehensive overview of all doctors, patients, and appointments

### 5. Audit Service
- View recent audit entries (last 10 or 20 actions)
- Clear audit log when needed
- Automatic logging of all user actions and database operations
- CSV format for easy analysis and reporting

## Database Schema

The application uses the following database tables:
- `medical_specialties` - Available medical specialties
- `doctors` - Doctor information and references
- `patients` - Patient information
- `appointments` - Appointment scheduling and status
- `addresses` - Address information for doctors and patients
- `contact_info` - Contact details (phone and email)

## Files Structure

```
ClinicApp/
├── src/                    # Java source files
│   ├── Main.java          # Main CLI application with audit integration
│   ├── AuditService.java  # Audit service for logging user actions
│   ├── DatabaseConnection.java # Database operations
│   └── [other model classes]
├── bin/                    # Compiled Java classes
├── lib/                    # Dependencies (PostgreSQL JDBC driver)
├── audit_log.csv          # Audit trail file (created at runtime)
├── schema.sql             # Database schema creation script
├── sample_data.sql        # Sample data for testing
├── DATABASE.md            # Database documentation
├── run.sh                 # Application launcher script
└── README.md              # This file
```

## Sample Data

The database comes pre-populated with:
- 9 medical specialties (General Practice, Cardiology, Dermatology, etc.)
- Sample doctors, patients, and appointments for testing

## Troubleshooting

1. **Database Connection Issues**:
   - Ensure PostgreSQL container is running: `docker ps`
   - Check if port 5432 is accessible: `docker port postgres`

2. **Compilation Errors**:
   - Verify JDBC driver is in `lib/` directory
   - Check Java version: `java -version`

3. **Runtime Errors**:
   - Ensure database schema is created: `psql -U admin -d pao -f schema.sql`
   - Check database connectivity from host system

## Development

To modify or extend the application:
1. Edit source files in `src/` directory
2. Recompile using the provided compilation command
3. Test with the CLI interface
4. Update database schema if needed (`schema.sql`)

For more detailed database information, see `DATABASE.md`.
