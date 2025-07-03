import streamlit as st
import pandas as pd

from utils.preprocessing import clean_transcription
from model.NER_model import extract_entities
from recommender import recommend_medications

# Set Streamlit page config
st.set_page_config(
    page_title="Clinical Decision Support System",
    layout="wide"
)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/mtsamples.csv")
    df.dropna(subset=['transcription'], inplace=True)
    df['transcription'] = df['transcription'].apply(clean_transcription)
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()

# Color map for entity types
ENTITY_COLORS = {
    "DISEASE": "#f03f3f",
    "TREATMENT": "#5be65b",
    "BODY_PART": "#3f83cb",
    "TEST": "#8b06f7",
    "PROCEDURE": "#7b767e",
    "MEDICAL_CONDITION": "#e7bf3e",
}

# Function to highlight entities in text
def highlight_entities(text, entities):
    if not entities:
        return text

    # Sort entities by appearance
    sorted_ents = sorted(entities, key=lambda e: e.get("start", 0))
    highlighted = ""
    last_idx = 0

    for ent in sorted_ents:
        word = ent["word"]
        label = ent["entity_group"]
        color = ENTITY_COLORS.get(label, "#ffffcc")  # default: pale yellow
        start = text.find(word, last_idx)
        end = start + len(word)

        if start == -1:
            continue  # skip if word not found

        # Append plain text + highlighted entity
        highlighted += text[last_idx:start]
        highlighted += f"<span style='background-color: {color}; padding:2px 4px; border-radius:4px;'>{word}</span>"
        last_idx = end

    highlighted += text[last_idx:]
    return highlighted

# App Title
st.title("🧠 Clinical Decision Support System (CDSS)")
st.write("Extract clinical entities from medical transcription samples using NLP.")

# Select transcription sample
sample = st.selectbox("📋 Select a sample transcription:", df['sample_name'].dropna().unique())

# Get selected text
text = df[df['sample_name'] == sample]['transcription'].values[0]

# Show full transcription text
st.subheader("📄 Original Transcription")
st.text_area("Clinical Note", value=text, height=300)

# Button to extract entities
if st.button("🚀 Extract Clinical Entities"):
    with st.spinner("Running biomedical NER model..."):
        entities = extract_entities(text)

    st.subheader("🔍 Highlighted Transcription")
    if not entities:
        st.info("No entities found in the text.")
        st.write(text)
    else:
        html = highlight_entities(text, entities)
        st.markdown(html, unsafe_allow_html=True)

        st.subheader("📊 Entity Breakdown")
        for ent in entities:
            st.markdown(f"- **{ent['entity_group']}** → `{ent['word']}` _(score: {ent['score']:.2f})_")

# After extracting NER entities - create recommender
transcription_text = st.text_area("Enter transcription", height=200)

if transcription_text.strip():
    entities = extract_entities(transcription_text)
    st.write('ent',entities)
    recommendations = recommend_medications(entities)

    st.subheader("💊 Medication Recommendations")
    if recommendations:
        for med in recommendations:
            st.markdown(f"- {med}")
    else:
        st.info("No recommendations available for detected conditions.")
else:
    st.write('Enter transcription first')