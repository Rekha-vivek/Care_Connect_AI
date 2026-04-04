import sqlite3
import pandas as pd


# ================= CONNECTION =================
def create_connection():
    return sqlite3.connect("careconnect.db")


# ================= CREATE TABLES =================
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT
    )
    """)

    # PATIENTS
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

    # DOCTORS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id TEXT PRIMARY KEY,
        name TEXT,
        specialization TEXT,
        available_time TEXT
    )
    """)

    # APPOINTMENTS (UPDATED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id TEXT PRIMARY KEY,
        patient_id TEXT,
        doctor_id TEXT,
        scheduled_time TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    # VITALS (UPDATED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        patient_id TEXT,
        temperature REAL,
        bp TEXT,
        pulse INTEGER,
        spo2 INTEGER,
        notes TEXT,
        recorded_at TEXT
    )
    """)

    # PRESCRIPTIONS (UPDATED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        prescription_id TEXT PRIMARY KEY,
        patient_id TEXT,
        doctor_id TEXT,
        medicine TEXT,
        dosage TEXT,
        instructions TEXT,
        prescribed_at TEXT,
        fulfilled TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= INSERT CSV DATA =================
def insert_data():
    conn = create_connection()

    # Load CSV
    users = pd.read_csv("Users.csv")
    patients = pd.read_csv("Patients_table.csv")
    doctors = pd.read_csv("Doctors_table.csv")
    appointments = pd.read_csv("Appointments.csv")
    vitals = pd.read_csv("Vitals.csv")
    prescriptions = pd.read_csv("Prescription.csv")

    # Clean column names
    users.columns = users.columns.str.lower()
    patients.columns = patients.columns.str.lower()
    doctors.columns = doctors.columns.str.lower()
    appointments.columns = appointments.columns.str.lower()
    vitals.columns = vitals.columns.str.lower()
    prescriptions.columns = prescriptions.columns.str.lower()

    # Insert into DB
    users.to_sql("users", conn, if_exists="replace", index=False)
    patients.to_sql("patients", conn, if_exists="replace", index=False)
    doctors.to_sql("doctors", conn, if_exists="replace", index=False)
    appointments.to_sql("appointments", conn, if_exists="replace", index=False)
    vitals.to_sql("vitals", conn, if_exists="replace", index=False)
    prescriptions.to_sql("prescriptions", conn, if_exists="replace", index=False)

    conn.close()


# ================= RUN =================
if __name__ == "__main__":
    create_tables()
    insert_data()