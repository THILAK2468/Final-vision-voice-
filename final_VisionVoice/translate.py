from settings import user_language

translations = {
    "te": {
        "car": "కారు",
        "person": "వ్యక్తి",
        "truck": "ట్రక్",
        "bus": "బస్సు",
        "motorbike": "మోటార్ బైక్",
        "pothole": "గుంత"
    },
    "hi": {
        "car": "गाड़ी",
        "person": "व्यक्ति",
        "truck": "ट्रक",
        "bus": "बस",
        "motorbike": "मोटरबाइक",
        "pothole": "गड्ढा"
    },
    "en": {}  # No translation needed
}

def translate_label(label):
    return translations.get(user_language, {}).get(label, label)