package ClinicApp.src;

public class Doctor extends Person {
    private MedicalSpecialty specialty;

    public Doctor(String firstName, String lastName, ContactInfo contactInfo, Address address,
            MedicalSpecialty specialty) {
        super(firstName, lastName, contactInfo, address);
        this.specialty = specialty;
    }

    public MedicalSpecialty getSpecialty() {
        return specialty;
    }

    @Override
    public String getRole() {
        return "Doctor";
    }

    @Override
    public String toString() {
        return "Doctor [" + super.toString() + ", Specialty: " + specialty.getName() + "]";
    }

}