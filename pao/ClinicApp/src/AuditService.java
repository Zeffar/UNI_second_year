package ClinicApp.src;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class AuditService {
    private static final String AUDIT_FILE_PATH = "audit_log.csv";
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static AuditService instance;
    
    private AuditService() {
        initializeAuditFile();
    }
    
    // Singleton pattern to ensure one instance
    public static synchronized AuditService getInstance() {
        if (instance == null) {
            instance = new AuditService();
        }
        return instance;
    }
    
    /**
     * Initialize the audit file with headers if it doesn't exist
     */
    private void initializeAuditFile() {
        Path auditPath = Paths.get(AUDIT_FILE_PATH);
        
        try {
            if (!Files.exists(auditPath)) {
                try (PrintWriter writer = new PrintWriter(new FileWriter(AUDIT_FILE_PATH))) {
                    writer.println("Action_name,Timestamp");
                }
                System.out.println("Audit log file created: " + AUDIT_FILE_PATH);
            }
        } catch (IOException e) {
            System.err.println("Error initializing audit file: " + e.getMessage());
        }
    }
    
    /**
     * Log an action to the audit file
     * @param actionName The name of the action performed
     */
    public void logAction(String actionName) {
        String timestamp = LocalDateTime.now().format(TIMESTAMP_FORMAT);
        
        try (PrintWriter writer = new PrintWriter(new FileWriter(AUDIT_FILE_PATH, true))) {
            writer.println(String.format("%s,%s", escapeCSV(actionName), timestamp));
        } catch (IOException e) {
            System.err.println("Error writing to audit file: " + e.getMessage());
        }
    }
    
    /**
     * Log an action with additional details
     * @param actionName The name of the action performed
     * @param details Additional details about the action
     */
    public void logActionWithDetails(String actionName, String details) {
        String actionWithDetails = actionName + " - " + details;
        logAction(actionWithDetails);
    }
    
    /**
     * Escape special characters in CSV fields
     * @param field The field to escape
     * @return Escaped field safe for CSV
     */
    private String escapeCSV(String field) {
        if (field == null) {
            return "";
        }
        
        // If field contains comma, quote, or newline, wrap in quotes and escape quotes
        if (field.contains(",") || field.contains("\"") || field.contains("\n")) {
            return "\"" + field.replace("\"", "\"\"") + "\"";
        }
        
        return field;
    }
    
    /**
     * Get the current audit file path
     * @return The path to the audit file
     */
    public String getAuditFilePath() {
        return AUDIT_FILE_PATH;
    }
    
    /**
     * Read and display recent audit entries
     * @param numberOfEntries Number of recent entries to display
     */
    public void displayRecentAuditEntries(int numberOfEntries) {
        try {
            Path auditPath = Paths.get(AUDIT_FILE_PATH);
            if (Files.exists(auditPath)) {
                var lines = Files.readAllLines(auditPath);
                System.out.println("\n--- Recent Audit Entries ---");
                System.out.println("Action Name | Timestamp");
                System.out.println("-".repeat(50));
                
                int startIndex = Math.max(1, lines.size() - numberOfEntries); // Skip header at index 0
                for (int i = startIndex; i < lines.size(); i++) {
                    String[] parts = lines.get(i).split(",", 2);
                    if (parts.length == 2) {
                        System.out.printf("%s | %s%n", parts[0], parts[1]);
                    }
                }
            } else {
                System.out.println("Audit file not found.");
            }
        } catch (IOException e) {
            System.err.println("Error reading audit file: " + e.getMessage());
        }
    }
    
    /**
     * Clear the audit log (keep headers)
     */
    public void clearAuditLog() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(AUDIT_FILE_PATH))) {
            writer.println("Action_name,Timestamp");
            System.out.println("Audit log cleared.");
        } catch (IOException e) {
            System.err.println("Error clearing audit file: " + e.getMessage());
        }
    }
}
