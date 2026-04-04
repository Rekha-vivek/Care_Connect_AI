# ================= RAG + NLP ENGINE =================

import re

# ================= PATIENT MEMORY (RAG) =================
patient_memory = {
    "P001": "Had fever and headache last week",
    "P002": "High BP patient",
    "P003": "Diabetes patient"
}

def get_patient_history(patient_id):
    return patient_memory.get(patient_id, "No history found")


# ================= CONDITION KEYWORDS =================
keywords = {
    "cardiac": ["cardiac", "heart"],
    "migraine": ["migraine", "headache"],
    "acidity": ["acidity", "gas"],
    "lung": ["lung", "respiratory"],
    "infection": ["infection", "inflammation"],
    "fever": ["fever"],
    "diabetes": ["glucose", "sugar"],
    "normal": ["normal", "no abnormalities", "within normal limits"]
}


# ================= CONDITION EXTRACTION =================
def extract_condition(text):
    text = str(text).lower()

    for condition, words in keywords.items():
        for word in words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text):
                return condition

    return "normal"


# ================= DOCTOR MAPPING =================
doctor_map = {
    "cardiac": "Cardiologist",
    "migraine": "Neurologist",
    "acidity": "Gastroenterologist",
    "lung": "Pulmonologist",
    "infection": "General Physician",
    "fever": "General Physician",
    "diabetes": "Endocrinologist",
    "normal": "General Physician"
}


# ================= DOCTOR EXTRACTION =================
def extract_doctor(text, condition):
    text = str(text).lower()

    # 🔥 direct keyword priority (strong signals)
    if "lung" in text:
        return "Pulmonologist"
    if "glucose" in text or "sugar" in text:
        return "Endocrinologist"
    if "brain" in text:
        return "Neurologist"

    # ✅ fallback
    return doctor_map.get(condition, "General Physician")