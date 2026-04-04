import streamlit as st
import pandas as pd
import datetime
import random
from chatbot import final_prediction
from ocr import extract_text_from_image
from rag import get_patient_history
from backend import view_doctors,book_appointment

st.set_page_config(
    page_title="CareConnect AI",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: white;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #1a1c23;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: white!important;
}
            
/* MAIN TEXT ONLY */
[data-testid="stAppViewContainer"] {
    color: white;
}

/* LABELS */
label {
    color: white !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #c77dff !important;
}

/* SELECT BOX (Navigation) */
div[data-baseweb="select"] > div {
    background-color: #7b2cbf !important;
    color: white !important;
    border-radius: 10px;
}

/* INPUT BOXES */
input, textarea {
    background-color: #1e1e2f !important;
    color: white !important;
    border: 1px solid #7b2cbf !important;
}

/* BUTTON */
.stButton>button {
    background-color: #9d4edd;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

/* BUTTON HOVER */
.stButton>button:hover {
    background-color: #c77dff;
    transform: scale(1.05);
}

/* HEADINGS */
h1, h2, h3 {
    color: #c77dff;
}

/* CARD STYLE */
.card {
    background-color: #1e1e2f;   /* dark card */
    color:#1e1e2f;
    padding: 10px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

/* SUCCESS */
.stSuccess {
    background-color: #1b5e20 !important;
    color: white;
}

/* WARNING */
.stWarning {
    background-color: #ff6f00 !important;
    color: white;
}

/* ERROR */
.stError {
    background-color: #b71c1c !important;
    color: white;
}
            
/* REMOVE TOP WHITE BAR */
header {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center;'>🩺 CareConnect AI</h1>
<h4 style='text-align: center;'>Smart Healthcare Assistant</h4>
<hr>
""", unsafe_allow_html=True)


menu = ["Chatbot", "View Doctors", "Book Appointment", "Add Vitals","Dashboard","Patient Details","Prescriptions","Upload Report", "Medical Reports",        # ✅ NEW
    "Discharge Summary","Admin Panel"]  
choice = st.sidebar.selectbox("Select Option", menu)

# CHATBOT
if choice == "Chatbot":

    st.subheader("🧠 AI Health Assistant")

    user_input = st.text_area("Describe your symptoms:")

    # 👉 Store response
    if "chat_response" not in st.session_state:
        st.session_state.chat_response = None

    # 🔥 First button
    if st.button("Get Suggestion"):
      
      if user_input.strip() == "":
        st.warning("Please enter symptoms")
      else:
        result = final_prediction(user_input)
        st.success(result)

    # 👉 SHOW RESPONSE AFTER BUTTON CLICK
    if st.session_state.chat_response:

        response = st.session_state.chat_response

        st.success(response["message"])

        if response.get("doctor"):

            # 🔥 SECOND BUTTON (NOW WORKS)
            if st.button(f"Book Appointment with {response['doctor']}"):

                import datetime
                import random

                doctor_map = {
                    "General Physician":"UD001",
                    "Cardiologist":"UD002",
                    "Neurologist":"UD003",
                    "Orthopedic":"UD004",
                    "Gastroenterologist":"UD005"
                }

                appointment_id = "A" + str(random.randint(100, 999))
                patient_id = "P001"
                doctor_id = doctor_map.get(response["doctor"], "UD001")
                date = datetime.date.today()

                book_appointment(appointment_id, patient_id, doctor_id, date)

                st.success("✅ Appointment booked successfully!")
                st.write(f"Doctor: {response['doctor']}")
                st.write(f"Date: {date}")

#VIEW DOCTORS
elif choice == "View Doctors":

    st.header("👨‍⚕️ Available Doctors")

    doctors = view_doctors()

    # Convert to DataFrame
    df = pd.DataFrame(doctors, columns=[
        "Doctor ID", "Name", "Specialization", "Available Time"
    ])

    if df.empty:
        st.warning("No doctors available")
    else:

        # 🔍 FILTER OPTION (NEW)
        specialization = st.selectbox(
            "Filter by Specialization",
            ["All"] + sorted(df["Specialization"].unique().tolist())
        )

        if specialization != "All":
            df = df[df["Specialization"] == specialization]

        # 🔍 SEARCH OPTION (NEW)
        search = st.text_input("Search Doctor by Name")

        # 📊 SHOW TABLE
        st.dataframe(df, use_container_width=True)

        # 🎯 SELECT DOCTOR
        selected = st.selectbox("Select Doctor", df["Name"])

        if selected:
            doc = df[df["Name"] == selected].iloc[0]

            st.success(f"""
            👨‍⚕️ Doctor Selected: {doc['Name']}
            🩺 Specialization: {doc['Specialization']}
            ⏰ Available Time: {doc['Available Time']}
            """)

            # 🔥 QUICK BOOK BUTTON
            if st.button("Book Appointment"):

                import datetime
                import random

                appointment_id = "A" + str(random.randint(100, 999))
                patient_id = "P001"
                doctor_id = doc["Doctor ID"]
                date = datetime.date.today()

                from backend import book_appointment
                book_appointment(appointment_id, patient_id, doctor_id, str(date))

                st.success("✅ Appointment booked successfully!")

#BOOK APPOINTMENTS
elif choice == "Book Appointment":

    st.subheader("📅 Book Appointment")

    doctors = view_doctors()
    if not doctors:
        st.warning("No doctors available")
    else:
        df = pd.DataFrame(doctors, columns=[
            "Doctor ID", "Name", "Specialization", "Available Time"
        ])

        col1, col2 = st.columns(2)

        with col1:
            patient_id = st.text_input("Patient ID")

        with col2:
            selected_doc = st.selectbox(
                "Select Doctor",
                df["Name"]
            )

        # Get doctor details
        doc_row = df[df["Name"] == selected_doc].iloc[0]
        doctor_id = doc_row["Doctor ID"]

        st.info(f"🩺 {doc_row['Specialization']}")
        st.info(f"⏰ {doc_row['Available Time']}")

        # Date + Time (IMPORTANT CHANGE)
        scheduled_time = st.datetime_input("Select Date & Time")

        appointment_id = "A" + str(random.randint(1000, 9999))

        if st.button("Book Appointment"):

            if not patient_id:
                st.error("Enter patient ID")

            else:
                book_appointment(
                    appointment_id,
                    patient_id,
                    doctor_id,
                    str(scheduled_time)
                )

                st.success("✅ Appointment booked successfully!")
                st.write(f"Appointment ID: {appointment_id}")
                st.write(f"Doctor: {selected_doc}")
                st.write(f"Time: {scheduled_time}")

# VITALS
elif choice == "Add Vitals":

    st.markdown("""
    <div style='padding:1px; background-color:#dfe391; border-radius:10px;'>
    <h2 style='font-size:20px; color:#c77dff;'>❤️ Add Patient Vitals</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.text_input("Patient ID")
        temperature = st.number_input("Temperature (°C)", step=0.1)
        bp = st.text_input("Blood Pressure (e.g., 120/80)")

    with col2:
        pulse = st.number_input("Pulse")
        spo2 = st.number_input("SpO2 (%)", min_value=0, max_value=100)
        notes = st.selectbox("Condition Notes", ["Normal", "Fever", "Low temp", "Stable", "Critical"])

    if st.button("Save Vitals"):

        if not patient_id:
            st.error("Enter patient ID")

        elif temperature < 30 or temperature > 45:
            st.error("⚠️ Temperature abnormal")

        elif pulse < 40 or pulse > 150:
            st.error("⚠️ Pulse abnormal")

        elif spo2 < 80:
            st.error("🚨 Very low SpO2!")

        else:
            from backend import add_vitals, predict_risk

            add_vitals(patient_id, temperature, bp, pulse, spo2, notes)

            st.success("✅ Vitals added successfully!")

            # 🔥 Risk Prediction
            risk = predict_risk(temperature, bp, pulse)

            if risk == "HIGH RISK":
                st.error("🚨 HIGH RISK detected!")

            elif risk == "MILD RISK":
                st.warning("⚠️ Mild Risk detected")

            else:
                st.success("✅ Patient is Normal")
            
# ================= DASHBOARD =================
elif choice == "Dashboard":

    st.markdown("## 📊 Healthcare Dashboard")

    import sqlite3
    conn = sqlite3.connect("careconnect.db")

    patients = pd.read_sql("SELECT * FROM patients", conn)
    appointments = pd.read_sql("SELECT * FROM appointments", conn)
    vitals = pd.read_sql("SELECT * FROM vitals", conn)

    conn.close()

    # ================= KPIs =================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👨‍⚕️ Total Patients", len(patients))

    with col2:
        st.metric("📅 Total Appointments", len(appointments))

    with col3:
        st.metric("❤️ Total Vitals Records", len(vitals))

    # ================= PATIENT ANALYSIS =================
    st.markdown("### 🧬 Disease Distribution")

    if not patients.empty:
        st.bar_chart(patients["medical_history"].value_counts())

    # ================= APPOINTMENT ANALYSIS =================
    st.markdown("### 📅 Appointment Status")

    if not appointments.empty:
        st.bar_chart(appointments["status"].value_counts())

    # ================= VITALS =================
    st.markdown("### ❤️ Vitals Trends")

    if not vitals.empty:

        vitals.columns = vitals.columns.str.lower()
        vitals = vitals.sort_values(by="recorded_at")

        st.write("🌡 Temperature Trend")
        st.line_chart(vitals["temperature"])

        st.write("🫁 SpO2 Trend")
        st.line_chart(vitals["spo2"])

        st.write("📈 BP Trend")
        try:
            bp_split = vitals["bp"].str.split("/", expand=True).astype(int)
            st.line_chart(bp_split)
        except:
            st.warning("BP format issue")

    # ================= ALERTS =================
    st.markdown("## 🚨 Critical Alerts")

    if not vitals.empty:

        latest = vitals.drop_duplicates(subset="patient_id", keep="last")

        alerts_found = False

        for _, row in latest.iterrows():

            temp = float(row["temperature"])
            pulse = int(row["pulse"])
            spo2 = int(row["spo2"])
            bp = str(row["bp"])

            if temp >= 38:
                st.error(f"🔥 High Fever → {row['patient_id']}")
                alerts_found = True

            if pulse >= 100:
                st.warning(f"💓 High Pulse → {row['patient_id']}")
                alerts_found = True

            try:
                systolic = int(bp.split("/")[0])
                if systolic >= 140:
                    st.error(f"💔 High BP → {row['patient_id']}")
                    alerts_found = True
            except:
                pass

            if spo2 < 95:
                st.error(f"🫁 Low SpO2 → {row['patient_id']}")
                alerts_found = True

        if not alerts_found:
            st.success("✅ All patients stable")

# ================= PATIENT DETAILS =================
elif choice == "Patient Details":

    st.subheader("👤 Patient Details")

    from backend import get_patient, get_patient_vitals, get_patient_appointments

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Search"):

        if not patient_id:
            st.warning("Enter patient ID")

        else:
            patient = get_patient(patient_id)

            if patient:

                # 👤 BASIC DETAILS
                st.markdown("### 👤 Basic Info")

                df = pd.DataFrame([patient], columns=[
                    "Patient ID","User ID","Age","Gender",
                    "Blood Group","Allergies","Medical History"
                ])
                st.dataframe(df, use_container_width=True)

                # ❤️ VITALS
                st.markdown("### ❤️ Vitals History")

                vitals_df = get_patient_vitals(patient_id)

                if not vitals_df.empty:
                    vitals_df.columns = vitals_df.columns.str.lower()
                    st.dataframe(vitals_df, use_container_width=True)
                else:
                    st.info("No vitals data found")

                # 📅 APPOINTMENTS
                st.markdown("### 📅 Appointment History")

                appt_df = get_patient_appointments(patient_id)

                if not appt_df.empty:
                    appt_df.columns = appt_df.columns.str.lower()
                    st.dataframe(appt_df, use_container_width=True)
                else:
                    st.info("No appointments found")

            else:
                st.error("Patient not found")

# ================= PRESCRIPTIONS =================
elif choice == "Prescriptions":

    st.subheader("💊 Prescription Management")

    from backend import add_prescription, get_prescriptions, view_doctors
    import random

    patient_id = st.text_input("Patient ID")

    # Doctor selection
    doctors = view_doctors()

    if doctors:
        df_doc = pd.DataFrame(doctors, columns=[
            "Doctor ID", "Name", "Specialization", "Available Time"
        ])

        selected_doc = st.selectbox("Select Doctor", df_doc["Name"])
        doc_row = df_doc[df_doc["Name"] == selected_doc].iloc[0]
        doctor_id = doc_row["Doctor ID"]

        st.info(f"🩺 {doc_row['Specialization']}")
    else:
        doctor_id = st.text_input("Doctor ID")

    # Fields
    medicine = st.text_input("Medicine")
    dosage = st.text_input("Dosage")
    instructions = st.text_area("Instructions")

    fulfilled = st.selectbox("Fulfilled", ["True", "False"])

    # SAVE
    if st.button("Save Prescription"):

        if not patient_id:
            st.error("Enter patient ID")

        elif not medicine:
            st.error("Enter medicine")

        else:
            prescription_id = "PR" + str(random.randint(1000, 9999))

            add_prescription(
                prescription_id,
                patient_id,
                doctor_id,
                medicine,
                dosage,
                instructions,
                fulfilled
            )

            st.success("✅ Prescription added!")

    # VIEW
    if st.button("View Prescriptions"):

        if not patient_id:
            st.warning("Enter patient ID")

        else:
            df = get_prescriptions(patient_id)

            if not df.empty:
                df.columns = df.columns.str.lower()
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No prescriptions found")

# =================MEDICAL REPORT OCR  =================
elif choice == "Upload Report":

    st.subheader("📄 Upload Medical Report (OCR)")

    from ocr import extract_text_from_image
    from backend import save_report
    import re

    uploaded_file = st.file_uploader("Upload Report Image", type=["png", "jpg", "jpeg"])
    patient_id = st.text_input("Enter Patient ID")

    if uploaded_file is not None:

        st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)

        if st.button("Extract & Analyze"):

            text = extract_text_from_image(uploaded_file)

            st.text_area("Extracted Text", text, height=200)

            # ================= EXTRACTION =================

            # BP
            bp_match = re.search(r'\b\d{2,3}/\d{2,3}\b', text)

            # Temperature (better logic)
            temp_match = re.search(r'\b(9[5-9]|10[0-5])(\.\d)?\b', text)

            bp = bp_match.group() if bp_match else "Not found"
            temperature = temp_match.group() if temp_match else "Not found"

            st.success(f"BP: {bp}")
            st.success(f"Temperature: {temperature}")

            # ================= ML =================
            result = final_prediction(text)
            st.success(result)

            # ================= SAVE =================
            if patient_id:

                save_report(patient_id, bp, temperature, text)

                st.success("✅ Report saved successfully!")

            else:
                st.error("Enter patient ID")


# ================= DISCHARGE SUMMARY =================
elif choice == "Discharge Summary":

    st.subheader("📋 Discharge Summary Analysis")

    import pandas as pd
    from rag import extract_condition, extract_doctor

    try:
        df = pd.read_csv("Discharge_summary.csv")

        # 🔥 CLEAN COLUMN NAMES (important)
        df.columns = df.columns.str.lower()

        # 🔥 APPLY NLP
        df["condition"] = df["summary_text"].apply(extract_condition)

        # 🔥 DOCTOR MAPPING
        df["recommended_doctor"] = df.apply(
            lambda row: extract_doctor(row["summary_text"], row["condition"]),
            axis=1
        )

        # ✅ SHOW RESULT
        st.dataframe(df, use_container_width=True)

        # ================= INSIGHTS =================
        st.markdown("### 📊 Condition Distribution")
        st.bar_chart(df["condition"].value_counts())

        st.markdown("### 👨‍⚕️ Doctor Distribution")
        st.bar_chart(df["recommended_doctor"].value_counts())

    except Exception as e:
        st.error(f"Error loading discharge summary: {e}")

# ================= ADMIN PANEL =================
elif choice == "Admin Panel":

    st.subheader("🛠 Admin Dashboard")

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("careconnect.db")

    # ================= DATABASE TABLES =================
    st.markdown("### 👤 Patients")
    st.dataframe(pd.read_sql("SELECT * FROM patients", conn), use_container_width=True)

    st.markdown("### 👨‍⚕️ Doctors")
    st.dataframe(pd.read_sql("SELECT * FROM doctors", conn), use_container_width=True)

    st.markdown("### 📅 Appointments")
    st.dataframe(pd.read_sql("SELECT * FROM appointments", conn), use_container_width=True)

    st.markdown("### 💊 Prescriptions")
    st.dataframe(pd.read_sql("SELECT * FROM prescriptions", conn), use_container_width=True)

    st.markdown("### ❤️ Vitals")
    st.dataframe(pd.read_sql("SELECT * FROM vitals", conn), use_container_width=True)

    conn.close()

    # ================= ADMIN LOGS (CSV) =================
    st.markdown("### 📜 Admin Activity Logs")

    try:
        logs_df = pd.read_csv("Admins.csv")

        # clean column names
        logs_df.columns = logs_df.columns.str.lower()

        st.dataframe(logs_df, use_container_width=True)

        # ================= INSIGHTS =================
        st.markdown("### 📊 Actions Distribution")
        st.bar_chart(logs_df["action"].value_counts())

        st.markdown("### 🎯 Target Entity Distribution")
        st.bar_chart(logs_df["target_entity"].value_counts())

    except:
        st.warning("Admins.csv not found")