#!/bin/bash
# Script to run the Clinic Application
cd /home/zeffar/github/UNI_second_year/pao/ClinicApp
echo "Starting Clinic Application..."
echo "Make sure PostgreSQL container is running on port 5432"
echo "Database: pao, User: admin, Password: admin"
echo ""
java -cp "lib/postgresql-42.7.1.jar:bin" ClinicApp.src.Main
