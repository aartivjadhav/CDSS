import pandas as pd
import re

pd.set_option('display.max_columns', None)

df = pd.read_csv('data\mtsamples.csv')

# preprocessing the transcription columns - removing spaces, removing ascii characters and removing dectation words
def clean_transcription(text):
    if pd.isna(text):
        return ""
    
    # Remove excess whitespace, tabs, newlines
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove weird non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # (Optional) Strip dictation tags if any
    text = re.sub(r'DICTATED.*|TRANSCRIBED.*', '', text, flags=re.IGNORECASE)
    
    return text

# Step 1: Clean
df['transcription'] = df['transcription'].apply(clean_transcription)

# Step 2: Drop blanks (if any left)
df = df[df['transcription'].str.strip() != ''].reset_index(drop=True)

print(df.transcription.isna().value_counts())
# Step 3: Use for NER
# entities = ner_pipeline(df['transcription'][0])
