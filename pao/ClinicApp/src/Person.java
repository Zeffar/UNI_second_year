package ClinicApp.src;

import java.util.Objects;

public abstract class Person {
    private static long idCounter = 0;
    protected long personId;
    protected String firstName;
    protected String lastName;
    protected ContactInfo contactInfo;
    protected Address address;

    public Person(String firstName, String lastName, ContactInfo contactInfo, Address address) {
        this.personId = ++idCounter;
        this.firstName = firstName;
        this.lastName = lastName;
        this.contactInfo = contactInfo;
        this.address = address;
    }

    public long getPersonId() {
        return personId;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getFullName() {
        return firstName + " " + lastName;
    }

    public ContactInfo getContactInfo() {
        return contactInfo;
    }

    public Address getAddress() {
        return address;
    }

    public void setContactInfo(ContactInfo contactInfo) {
        this.contactInfo = contactInfo;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public abstract String getRole();

    @Override
    public String toString() {
        return "ID: " + personId + ", Name: " + getFullName() +
                ", Contact: [" + contactInfo + "], Address: [" + address + "]";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        Person person = (Person) o;
        return personId == person.personId;
    }

    @Override
    public int hashCode() {
        return Objects.hash(personId);
    }
}