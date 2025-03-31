package ClinicApp.src;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Patient extends Person {
    private LocalDate dateOfBirth;

    public Patient(String firstName, String lastName, ContactInfo contactInfo, Address address, LocalDate dateOfBirth) {
        super(firstName, lastName, contactInfo, address);
        this.dateOfBirth = dateOfBirth;
    }

    public LocalDate getDateOfBirth() {
        return dateOfBirth;
    }

    @Override
    public String getRole() {
        return "Patient";
    }

    @Override
    public String toString() {
        DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE; 
        return "Patient [" + super.toString() + ", DOB: "
                + (dateOfBirth != null ? dateOfBirth.format(formatter) : "N/A") + "]";
    }

}