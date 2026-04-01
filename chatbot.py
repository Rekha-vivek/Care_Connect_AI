from nlp_engine import process_input

def chatbot_response(user_input):

    result = process_input(user_input)

    intent = result.get("intent")
    entities = result.get("entities", {})
    symptom = entities.get("symptom")

    user_input = user_input.lower()

    # 🔥 Smart keyword detection
    keywords = {
         "fever": ["fever", "high temperature", "hot body"],
         "headache": ["headache", "head pain", "migraine"],
         "chest pain": ["chest pain", "tight chest", "heart pain"],
         "cough": ["cough", "dry cough"],
         "stomach pain": ["stomach", "abdominal", "gas pain"],
         "back pain": ["back pain", "backpain", "spine pain"],
         "fatigue": ["tired", "fatigue", "weak", "no energy"],
         }

    if not symptom:
        for key, words in keywords.items():
            for word in words:
                if word in user_input:
                    symptom = key
                    break

    # 🚀 Smart Responses
    if symptom == "fever":
        return {
        "message": "🤒 You may have fever.",
        "doctor": "General Physician"
    }

    elif symptom == "headache":
        return {
        "message":"head ache detected.",
        "doctor":"Neurologist"
    }
  
    elif symptom == "chest pain":
        return {
        "message": "🚨 Serious chest pain!",
        "doctor": "Cardiologist"
    }

    elif symptom == "cough":
        return {
        "message": "cough detected.",
        "doctor": "General Physician"
         }
  
    elif symptom == "stomach pain":
        return {
        "message": "stomach ache detected.",
        "doctor":"Gastroenterologist "
         }

    elif symptom == "backpain":
         return {
        "message": "🩻 Back pain detected.",
        "doctor": "Orthopedic"
         }
    
    elif symptom == "fatigue":
        return {
        "message": "fatigue detected.",
        "doctor": "General Physician"
         }
  
    elif symptom:
         return {
            "message": f"⚠️ Detected symptom: {symptom}. Please consult a doctor.",
            "doctor": "General Physician"
        }
    
    else:
        return {
        "message": "🤖 Could not understand",
        "doctor": None
    }