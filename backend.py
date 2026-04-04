import sqlite3
import pandas as pd
from datetime import datetime

# ================= CONNECTION =================
def create_connection():
    return sqlite3.connect('careconnect.db')


# ================= CREATE TABLES =================
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Vitals Table
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

    conn.commit()
    conn.close()


# ================= DOCTORS =================
def view_doctors():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT doctor_id, name, specialization, available_time 
    FROM doctors
    """)

    doctors = cursor.fetchall()
    conn.close()

    return doctors


# ================= APPOINTMENTS =================
def book_appointment(appointment_id, patient_id, doctor_id, scheduled_time):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO appointments 
    (Appointment_id, Patient_id, Doctor_id, Scheduled_time, Status, Created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        appointment_id,
        patient_id,
        doctor_id,
        scheduled_time,
        "Scheduled",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ================= VITALS =================
def add_vitals(patient_id, temperature, bp, pulse, spo2, notes):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO vitals 
    (patient_id, temperature, bp, pulse, spo2, notes, recorded_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        temperature,
        bp,
        pulse,
        spo2,
        notes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_vitals_history():
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM vitals", conn)
    conn.close()
    return df


def get_patient_vitals(patient_id):
    conn = create_connection()
    df = pd.read_sql("""
        SELECT * FROM vitals
        WHERE patient_id = ?
        ORDER BY recorded_at DESC
    """, conn, params=(patient_id,))
    conn.close()
    return df


# ================= PATIENT =================
def get_patient(patient_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    patient = cursor.fetchone()

    conn.close()
    return patient


# ================= APPOINTMENT HISTORY =================
def get_patient_appointments(patient_id):
    conn = create_connection()
    df = pd.read_sql("""
        SELECT * FROM appointments
        WHERE Patient_id = ?
        ORDER BY Scheduled_time DESC
    """, conn, params=(patient_id,))
    conn.close()
    return df


# ================= RISK =================
def predict_risk(temperature, bp, pulse):
    try:
        systolic = int(bp.split("/")[0])
    except:
        systolic = 0

    if temperature >= 39 or systolic >= 160 or pulse >= 120:
        return "HIGH RISK"
    elif temperature >= 38 or systolic >= 140 or pulse >= 100:
        return "MILD RISK"
    else:
        return "NORMAL"
    
# ================= PRESCRIPTIONS =================
def add_prescription(prescription_id, patient_id, doctor_id, medicine, dosage, instructions, fulfilled):
    conn = create_connection()
    cursor = conn.cursor()

    from datetime import datetime

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        Prescription_id TEXT,
        Patient_id TEXT,
        Doctor_id TEXT,
        Medicine TEXT,
        Dosage TEXT,
        Instructions TEXT,
        Prescribed_at TEXT,
        Fulfilled TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO prescriptions 
    (Prescription_id, Patient_id, Doctor_id, Medicine, Dosage, Instructions, Prescribed_at, Fulfilled)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prescription_id,
        patient_id,
        doctor_id,
        medicine,
        dosage,
        instructions,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        fulfilled
    ))

    conn.commit()
    conn.close()


def get_prescriptions(patient_id):
    conn = create_connection()
    df = pd.read_sql("""
        SELECT * FROM prescriptions
        WHERE Patient_id = ?
        ORDER BY Prescribed_at DESC
    """, conn, params=(patient_id,))
    conn.close()
    return df

# ================= REPORTS =================
def save_report(patient_id, bp, temperature, raw_text):
    conn = create_connection()
    cursor = conn.cursor()

    from datetime import datetime

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        patient_id TEXT,
        bp TEXT,
        temperature TEXT,
        raw_text TEXT,
        recorded_at TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO reports 
    (patient_id, bp, temperature, raw_text, recorded_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        bp,
        temperature,
        raw_text,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()