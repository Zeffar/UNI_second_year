# Audit Service Documentation

## Overview
The Audit Service provides comprehensive logging of all user actions and database operations in the Medical Cabinet Appointment System. It creates a detailed audit trail that can be used for compliance, debugging, and system monitoring purposes.

## Features

### 📝 **Comprehensive Logging**
- **Menu Navigation**: Logs when users access different sections (Doctor Operations, Patient Operations, etc.)
- **Operation Initiation**: Logs when users start specific operations (Add New Doctor, Schedule Appointment, etc.)
- **Database Operations**: Logs successful database operations with detailed information
- **Application Lifecycle**: Logs application start and exit

### 📊 **CSV Format**
- **File**: `audit_log.csv` (created automatically in application root directory)
- **Headers**: Action_name, Timestamp
- **Timestamp Format**: YYYY-MM-DD HH:mm:ss
- **CSV Escaping**: Handles special characters in action descriptions

### 🔍 **Audit Viewing**
- View recent audit entries (last 10 or 20)
- Clear audit log when needed
- Real-time audit entry display
- Formatted output for easy reading

## Audit Entry Types

### Application Lifecycle
- `APPLICATION_STARTED` - Application startup
- `APPLICATION_EXITED` - Application shutdown

### Menu Navigation
- `ACCESSED_DOCTOR_OPERATIONS` - User accessed doctor menu
- `ACCESSED_PATIENT_OPERATIONS` - User accessed patient menu
- `ACCESSED_APPOINTMENT_OPERATIONS` - User accessed appointment menu
- `VIEWED_ALL_DATA` - User viewed complete data overview

### Operation Initiation
- `ADD_NEW_DOCTOR_INITIATED` - User started adding a new doctor
- `ADD_NEW_PATIENT_INITIATED` - User started adding a new patient
- `SCHEDULE_NEW_APPOINTMENT_INITIATED` - User started scheduling appointment
- `UPDATE_APPOINTMENT_STATUS_INITIATED` - User started updating appointment status

### Database Operations (with details)
- `DOCTOR_ADDED_TO_DATABASE` - Doctor successfully added to database
  - Details: Doctor name, ID, specialty
- `PATIENT_ADDED_TO_DATABASE` - Patient successfully added to database
  - Details: Patient name, ID, date of birth
- `APPOINTMENT_SCHEDULED_IN_DATABASE` - Appointment successfully scheduled
  - Details: Appointment ID, doctor ID, patient ID, date/time, reason
- `APPOINTMENT_STATUS_UPDATED` - Appointment status successfully updated
  - Details: Appointment ID, new status

### Audit Management
- `VIEWED_AUDIT_LOG` - User accessed audit log menu
- `VIEWED_RECENT_AUDIT_10` - User viewed last 10 audit entries
- `VIEWED_RECENT_AUDIT_20` - User viewed last 20 audit entries
- `AUDIT_LOG_CLEARED` - User cleared the audit log

## Technical Implementation

### Singleton Pattern
```java
AuditService auditService = AuditService.getInstance();
```
- Ensures single instance across the application
- Thread-safe implementation
- Automatic file initialization

### Logging Methods
```java
// Simple action logging
auditService.logAction("ACTION_NAME");

// Action logging with details
auditService.logActionWithDetails("ACTION_NAME", "Additional details");
```

### CSV Safety
- Automatic CSV escaping for special characters
- Handles commas, quotes, and newlines in action descriptions
- Proper quoting and escape sequence handling

## Usage Examples

### Basic Action Logging
```java
auditService.logAction("USER_LOGIN");
```

### Detailed Operation Logging
```java
auditService.logActionWithDetails("DOCTOR_ADDED_TO_DATABASE", 
    String.format("Doctor: %s %s, ID: %d, Specialty: %s", 
        firstName, lastName, doctorId, specialty.getName()));
```

### Viewing Audit Entries
```java
auditService.displayRecentAuditEntries(10);
```

### Clearing Audit Log
```java
auditService.clearAuditLog();
```

## File Location and Format

### File Path
- **Location**: Application root directory
- **Filename**: `audit_log.csv`
- **Created**: Automatically on first application run

### CSV Format Example
```csv
Action_name,Timestamp
APPLICATION_STARTED,2025-06-04 11:41:59
ACCESSED_DOCTOR_OPERATIONS,2025-06-04 11:41:59
"DOCTOR_ADDED_TO_DATABASE - Doctor: John Smith, ID: 5, Specialty: Cardiology",2025-06-04 11:42:15
APPLICATION_EXITED,2025-06-04 11:42:30
```

## Integration Points

### Main Application
- Integrated into `Main.java` at all major decision points
- Menu navigation logging
- Operation initiation logging
- Successful database operation logging

### Database Operations
- Post-insertion logging for doctors, patients, appointments
- Status update logging for appointments
- Includes relevant entity details in audit entries

## Benefits

### 🔒 **Compliance**
- Complete audit trail for healthcare data operations
- Timestamped evidence of all system interactions
- Detailed operation logging for regulatory requirements

### 🐛 **Debugging**
- Track user actions leading to issues
- Identify operation patterns and bottlenecks
- Monitor system usage and performance

### 📈 **Analytics**
- Usage pattern analysis
- Operation frequency tracking
- System adoption metrics

### 🛡️ **Security**
- Track unauthorized access attempts
- Monitor data modification patterns
- Audit trail for incident investigation

## Maintenance

### Log Rotation
- Manual clearing through application menu
- Consider implementing automatic rotation for production use
- Archive old logs before clearing for long-term retention

### Performance
- Minimal performance impact due to append-only writes
- Consider file size monitoring for high-volume environments
- CSV format allows easy processing with standard tools

## Future Enhancements

### Potential Improvements
- User authentication logging
- Failed operation attempt logging
- Log rotation and archiving
- Integration with external logging systems
- Real-time audit monitoring dashboard
- Audit log encryption for sensitive environments

## Security Considerations

### File Protection
- Ensure audit log file has appropriate permissions
- Consider encrypting audit logs in production
- Implement secure log storage and backup procedures

### Data Privacy
- Audit logs contain sensitive medical information
- Follow HIPAA and other healthcare privacy regulations
- Implement proper access controls for audit log viewing
