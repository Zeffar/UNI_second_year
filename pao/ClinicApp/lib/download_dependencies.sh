#!/bin/bash
# Download PostgreSQL JDBC driver
echo "Downloading PostgreSQL JDBC driver..."
wget -O postgresql-42.7.1.jar https://jdbc.postgresql.org/download/postgresql-42.7.1.jar
echo "JDBC driver downloaded to lib/postgresql-42.7.1.jar"
echo "To compile with JDBC driver, use:"
echo "javac -cp \"lib/postgresql-42.7.1.jar:src\" src/*.java -d bin/"
echo "To run with JDBC driver, use:"
echo "java -cp \"lib/postgresql-42.7.1.jar:bin\" ClinicApp.src.Main"
