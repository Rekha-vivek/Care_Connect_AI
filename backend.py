import sqlite3

def create_connection():
    conn = sqlite3.connect("careconnect.db")
    return conn

#view doctors
def view_doctors():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()

    conn.close()
    return doctors

#book appointment 

def book_appointment(appointment_id, patient_id, doctor_id, date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO appointments (appointment_id, patient_id, doctor_id, date, status)
    VALUES (?, ?, ?, ?, ?)
    """, (appointment_id, patient_id, doctor_id, date, "Scheduled"))

    conn.commit()
    conn.close()

#add vitals

def add_vitals(patient_id, temperature, bp, pulse):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO vitals (patient_id, temperature, bp, pulse)
    VALUES (?, ?, ?, ?)
    """, (patient_id, temperature, bp, pulse))

    conn.commit()
    conn.close()

def get_vitals_history():
    import sqlite3
    import pandas as pd

    conn = create_connection()
    df = pd.read_sql("SELECT * FROM vitals", conn)
    conn.close()

    # ✅ FIX COLUMN CASE ISSUE
    df.columns = df.columns.str.lower()

    return df

#get patient

def get_patient(patient_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE patient_id=?", (patient_id,))
    patient = cursor.fetchone()

    conn.close()
    return patient

def predict_risk(temperature, bp, pulse):
    try:
        systolic = int(bp.split("/")[0])
    except:
        systolic = 0

    # Rules
    if temperature >= 39 or systolic >= 160 or pulse >= 120:
        return "HIGH RISK"

    elif temperature >= 38 or systolic >= 140 or pulse >= 100:
        return "MILD RISK"

    else:
        return "NORMAL"
