import json

# Load disease-medication mapping from file
try:
    with open("data/disease_medication_map.json") as f:
        disease_med_map = json.load(f)
except json.JSONDecodeError as e:
    print("❌ JSON decoding failed:", e)
    disease_med_map = {}

def recommend_medications(entities):
    recommendations = set()
    for ent in entities:
        if ent["entity_group"] in ["DISEASE", "MEDICAL_CONDITION","Disease_disorder","Sign_symptom"]:
            disease = ent["word"].lower().strip()

            # Simple normalization
            for key in disease_med_map.keys():
                if key in disease:
                    for med in disease_med_map[key]:
                        recommendations.add(med)
    return list(recommendations)
