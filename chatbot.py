from nlp_engine import process_input

def chatbot_response(user_input):
    result = process_input(user_input)

    intent = result["intent"]
    symptom = result["entities"].get("symptom")

    if intent == "symptom_check":
        if not symptom:
            return "Please clearly mention your symptoms"

    elif symptom == "fever":
        return "You may have fever. Consult General Physician."

    elif symptom == "headache":
        return "Possible migraine. Consult Neurologist."

    elif symptom == "chest pain":
        return "Consult Cardiologist immediately."

    elif symptom == "cough":
        return "Possible infection. Consult General Physician."

    else:
        return "Please provide more details"