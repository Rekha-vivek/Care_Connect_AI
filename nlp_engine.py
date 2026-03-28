import re

def extract_entities(text):
    text = text.lower()

    symptoms = ["fever", "headache", "diabetes", "cough", "chest pain"]

    detected_symptom = None
    for s in symptoms:
        if s in text:
            detected_symptom = s
            break

    duration = None
    match = re.search(r'(\d+)\s*day', text)
    if match:
        duration = match.group()

    return {
        "symptom": detected_symptom,
        "duration": duration
    }

def detect_intent(text):
    text = text.lower()

    if any(word in text for word in ["pain", "fever", "headache", "sick"]):
        return "symptom_check"
    elif "appointment" in text:
        return "appointment_booking"
    else:
        return "unknown"

def process_input(text):
    intent = detect_intent(text)
    entities = extract_entities(text)

    return {
        "intent": intent,
        "entities": entities
    }