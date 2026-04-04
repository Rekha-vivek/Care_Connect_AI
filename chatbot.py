import re

# 🔹 Clean Text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s/]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 🔹 Keywords
keywords = {
    "cardiac": ["cardiac", "heart"],
    "migraine": ["migraine", "headache"],
    "acidity": ["acidity"],
    "lung": ["lung"],
    "infection": ["infection", "inflammation"],
    "fever": ["fever"],
    "diabetes": ["glucose", "sugar"],
    "normal": ["normal", "no abnormalities"]
}


# 🔹 Condition Detection
def extract_condition(text):
    text = clean_text(text)

    for condition, words in keywords.items():
        for word in words:
            if re.search(r'\b' + word + r'\b', text):
                return condition

    return "normal"


# 🔹 Doctor Mapping
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


# 🔹 Final Prediction
def final_prediction(text):
    text = clean_text(text)

    condition = extract_condition(text)
    doctor = doctor_map.get(condition, "General Physician")

    return f"""
🩺 CareConnect AI Result

Condition: {condition.upper()}

Recommended Doctor: {doctor}
"""