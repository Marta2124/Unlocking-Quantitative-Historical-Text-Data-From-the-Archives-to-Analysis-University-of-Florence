import spacy
import pandas as pd
from pathlib import Path

# Path to trained model
model_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_4B_Training_and_Implementation/model/model-best"

# Load the trained model
nlp_model = spacy.load(model_path)

# Load CSV
csv_file = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_4B_Training_and_Implementation/sample_1870_1920_ner_people_regex_existing_spacy.csv"
df = pd.read_csv(csv_file)

# Extract entities
def extract_entities(text):
    doc = nlp_model(text)
    entities = [ent.text for ent in doc.ents]
    return " | ".join(entities)

df['tailored_entities'] = df['text'].apply(extract_entities)

# Save updated CSV
output_folder = Path("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_4B_Training_and_Implementation/output")
output_folder.mkdir(exist_ok=True)
output_file = output_folder / "sample_1870_1920_tailored_entities.csv"
df.to_csv(output_file, index=False)

print(f"Saved updated CSV to: {output_file}")

