from transformers import pipeline

# Load medical NER model from Hugging Face
ner_pipeline = pipeline(
    "ner",
    model="d4data/biomedical-ner-all",
    tokenizer="d4data/biomedical-ner-all",
    aggregation_strategy="simple"
)

def extract_entities(text):
    return ner_pipeline(text)
