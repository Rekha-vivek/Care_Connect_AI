import sqlite3
import pandas as pd

def create_connection():
    conn = sqlite3.connect("careconnect.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()


    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT
    )
    """)

    # Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        user_id TEXT,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        allergies TEXT,
        medical_history TEXT
    )
    """)

    # Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id TEXT PRIMARY KEY,
        name TEXT,
        specialization TEXT,
        available_time TEXT
    )
    """)

    # Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id TEXT PRIMARY KEY,
        patient_id TEXT,
        doctor_id TEXT,
        date TEXT,
        status TEXT
    )
    """)

    # Vitals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        patient_id TEXT,
        temperature REAL,
        bp TEXT,
        pulse INTEGER
    )
    """)

    # Prescriptions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id TEXT PRIMARY KEY,
        patient_id TEXT,
        doctor_id TEXT,
        medicine TEXT,
        dosage TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

# ✅ INSERT DATA FUNCTION 
def insert_data():
    conn = create_connection()

    users = pd.read_csv("Users.csv")
    patients = pd.read_csv("Patients_table.csv")
    doctors = pd.read_csv("Doctors_table.csv")
    appointments = pd.read_csv("Appointments.csv")
    vitals = pd.read_csv("Vitals.csv")
    prescriptions = pd.read_csv("Prescription.csv")

    users.to_sql("users", conn, if_exists="replace", index=False)
    patients.to_sql("patients", conn, if_exists="replace", index=False)
    doctors.to_sql("doctors", conn, if_exists="replace", index=False)
    appointments.to_sql("appointments", conn, if_exists="replace", index=False)
    vitals.to_sql("vitals", conn, if_exists="replace", index=False)
    prescriptions.to_sql("prescriptions", conn, if_exists="replace", index=False)

    conn.close()

# ✅ MAIN EXECUTION
if __name__ == "__main__":
    create_tables()
    insert_data()

