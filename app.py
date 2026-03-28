import streamlit as st
import pandas as pd
from backend import view_doctors, book_appointment, get_patient, add_vitals,get_vitals_history
from chatbot import chatbot_response
from backend import predict_risk

st.set_page_config(
    page_title="CareConnect AI",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #0d47a1;
    font-weight: bold;
}

/* Buttons */
.stButton>button {
    background-color: #0d47a1;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

/* Success box */
.stSuccess {
    background-color: #e8f5e9;
    border-radius: 10px;
}

/* Warning */
.stWarning {
    background-color: #fff3e0;
    border-radius: 10px;
}

/* Error */
.stError {
    background-color: #ffebee;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center;'>🩺 CareConnect AI</h1>
<h4 style='text-align: center;'>Smart Healthcare Assistant</h4>
<hr>
""", unsafe_allow_html=True)

menu = ["Chatbot", "View Doctors", "Book Appointment", "Add Vitals","Dashboard","Patient Details","Prescriptions","Upload Report"]
choice = st.sidebar.selectbox("Select Option", menu)
#CHATBOT
if choice == "Chatbot":
    st.subheader("🤖 AI Health Assistant")

    user_input = st.text_area("Describe your symptoms:")

    if st.button("Get Suggestion"):
        if user_input.strip() == "":
            st.warning("Please enter symptoms")
        else:
            response = chatbot_response(user_input)
            st.success(response)

#VIEW DOCTORS
elif choice == "View Doctors":
    st.header("Available Doctors")

    doctors = view_doctors()

    df = pd.DataFrame(doctors, columns=["Doctor ID","Name","Specialization","Available Time"])
    st.dataframe(df, use_container_width=True)

#BOOK APPOINTMENTS
elif choice == "Book Appointment":
    st.subheader("📅 Book Appointment")

    col1, col2 = st.columns(2)

    with col1:
        appointment_id = st.text_input("Appointment ID")
        patient_id = st.text_input("Patient ID")

    with col2:
        doctor_id = st.text_input("Doctor ID")
        date = st.date_input("Select Date")

    if st.button("Book Appointment"):
        if appointment_id and patient_id and doctor_id:
            book_appointment(appointment_id, patient_id, doctor_id, str(date))
            st.success("✅ Appointment booked successfully!")
        else:
            st.error("Please fill all fields")

# ADD VITALS
elif choice == "Add Vitals":

    st.markdown("""
    <div style='padding:20px; background-color:white; border-radius:15px; 
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);'>
    <h2>❤️ Add Patient Vitals</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.text_input("Patient ID", key="vitals_patient")
        temperature = st.number_input("Temperature", key="vitals_temp")

    with col2:
        bp = st.text_input("Blood Pressure (e.g., 120/80)", key="vitals_bp")
        pulse = st.number_input("Pulse", key="vitals_pulse")

    if st.button("Save Vitals"):

        if not patient_id:
            st.error("Enter patient ID")

        elif temperature < 30 or temperature > 45:
            st.error("⚠️ Temperature seems abnormal")

        elif pulse < 40 or pulse > 150:
            st.error("⚠️ Pulse seems abnormal")

        else:
            add_vitals(patient_id, temperature, bp, pulse)

            st.success("✅ Vitals added successfully!")
            st.balloons()

            # 🔥 AI RISK
            risk = predict_risk(temperature, bp, pulse)

            if risk == "HIGH RISK":
                st.error("🚨 HIGH RISK detected! Immediate attention needed")

            elif risk == "MILD RISK":
                st.warning("⚠️ Mild Risk detected")

            else:
                st.success("✅ Patient is Normal") 
            
#DASHBOARD
elif choice == "Dashboard":

    st.markdown("## 📊 Healthcare Dashboard")

    import sqlite3
    conn = sqlite3.connect("careconnect.db")

    patients = pd.read_sql("SELECT * FROM patients", conn)
    appointments = pd.read_sql("SELECT * FROM appointments", conn)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("👨‍⚕️ Total Patients", len(patients))

    with col2:
        st.metric("📅 Total Appointments", len(appointments))

    st.write("### 📊 Disease Distribution")
    if not patients.empty:
        st.bar_chart(patients['Medical_history'].value_counts())

    st.write("### 📊 Appointment Status")
    if not appointments.empty:
        st.bar_chart(appointments['Status'].value_counts())

    conn.close()

    # ================= VITALS =================
    st.markdown("## 🩺 Patient Vitals History")

    vitals = get_vitals_history()

    if not vitals.empty:

        st.dataframe(vitals, use_container_width=True)

        st.write("### 📈 BP Trend")
        bp_split = vitals["bp"].str.split("/", expand=True).astype(int)
        st.line_chart(bp_split)

        st.write("### 🌡 Temperature Trend")
        st.line_chart(vitals["temperature"])

        # ================= ALERTS =================
        st.markdown("## 🚨 Alerts")

        vitals = vitals.drop_duplicates(subset="patient_id", keep="last")

        alerts_found = False

        for _, row in vitals.iterrows():

            patient = row["patient_id"]
            temp = float(row["temperature"])
            pulse = int(row["pulse"])
            bp = str(row["bp"])

            if temp >= 38:
                st.error(f"🔥 HIGH FEVER → Patient {patient} ({temp}°C)")
                alerts_found = True

            if pulse >= 100:
                st.warning(f"💓 HIGH PULSE → Patient {patient} ({pulse})")
                alerts_found = True

            try:
                systolic = int(bp.split("/")[0])
                if systolic >= 140:
                    st.error(f"💔 HIGH BP → Patient {patient} ({bp})")
                    alerts_found = True
            except:
                pass

        if not alerts_found:
            st.success("✅ All patients are normal")

# ================= PATIENT DETAILS =================
elif choice == "Patient Details":
    st.subheader("👤 Patient Details")

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Search"):
        patient = get_patient(patient_id)

        if patient:
            df = pd.DataFrame([patient], columns=[
                "Patient ID","User ID","Age","Gender","Blood Group","Allergies","Medical History"
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Patient not found")


#PRESCRIPTION
elif choice == "Prescriptions":
    st.subheader("💊 Add Prescription")

    patient_id = st.text_input("Patient ID", key="pres_patient")
    doctor_id = st.text_input("Doctor ID", key="pres_doc")
    medicine = st.text_input("Medicine", key="pres_med")
    dosage = st.text_input("Dosage", key="pres_dosage")
    date = st.date_input("Date", key="pres_date")

    if st.button("Save Prescription"):
        import sqlite3
        conn = sqlite3.connect("careconnect.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO prescriptions VALUES (?, ?, ?, ?, ?, ?)
        """, ("PR"+patient_id, patient_id, doctor_id, medicine, dosage, str(date)))

        conn.commit()
        conn.close()

        st.success("Prescription added!")

    # VIEW HISTORY
    if st.button("View Prescriptions"):
        import sqlite3
        conn = sqlite3.connect("careconnect.db")
        df = pd.read_sql(f"SELECT * FROM prescriptions WHERE patient_id='{patient_id}'", conn)
        st.dataframe(df)
        conn.close()

# UPLOAD REPORT (OCR)
elif choice == "Upload Report":
    st.subheader("📄 Upload Medical Report (OCR)")

    uploaded_file = st.file_uploader("Upload Report Image", type=["png", "jpg", "jpeg"])
    patient_id = st.text_input("Enter Patient ID")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)

        if st.button("Extract Data"):
            from PIL import Image
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = r"D:\OCR\tesseract.exe"
            import re

            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)

            st.text_area("Extracted Text", text, height=200)

            # Extract BP
            bp_match = re.search(r'\b\d{2,3}/\d{2,3}\b', text)

            # Extract Temperature
            numbers = re.findall(r'\b\d{2,3}\.\d\b', text)

            temperature = None
            for num in numbers:
                val = float(num)
                if 95 <= val <= 105:
                    temperature = num
                    break

            bp = bp_match.group() if bp_match else "Not found"
            temperature = temperature if temperature else "Not found"

            st.success(f"BP: {bp}")
            st.success(f"Temperature: {temperature}")

            # Save to DB
            if st.button("Save Report Data"):
                from backend import save_report

                if patient_id:
                    save_report(patient_id, bp, temperature)
                    st.success("✅ Report data saved!")
                else:
                    st.error("Enter patient ID")