# Import necessary libraries
import spacy
from spacy.cli.download import download
import pandas as pd

# Download/load the SpaCy English model (only needs once)
download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Read the CSV file
cc_1870_1920 = pd.read_csv(
    "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_3_Using_Existing_Spacy_Model/cc_1870_1920_with_regex.csv"
)

# Extract PERSON entities and join them with "|"
def extract_people_pipe(text):
    doc = nlp(str(text))
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return "|".join(people)

# Create a single column with all PERSON entities
cc_1870_1920["people_spacy_model"] = cc_1870_1920["text"].apply(extract_people_pipe)

# Preview results
print(cc_1870_1920[["text", "people_spacy_model"]].head())

# Save to new CSV
cc_1870_1920.to_csv(
    "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_3_Using_Existing_Spacy_Model/output/sample_1870_1920_ner_people_regex_existing_spacy.csv",
    index=False
)

