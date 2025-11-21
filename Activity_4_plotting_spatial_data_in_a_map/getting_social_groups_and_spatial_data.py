import spacy
import pandas as pd

# -----------------------------
# 1. Load BOTH tailored models
# -----------------------------
people_model_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/model/model-best"
space_model_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_3_running_the_model_to_extract_social_groups/model-best_24_06_2023_space_0.87"

nlp_people = spacy.load(people_model_path)
nlp_space = spacy.load(space_model_path)

# -----------------------------
# 2. Load the dataset
# -----------------------------
data_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/sample_1870_1920_long_tailored_entities.csv"
df = pd.read_csv(data_path)

# -----------------------------
# 3. Apply PEOPLE model to column "People"
#    Apply SPACE model to column "text"
# -----------------------------
preds = []
people_entities = []
space_entities = []

for idx, row in df.iterrows():

    # ========== PEOPLE MODEL on df["People"] ==========
    people_text = row["People"]

    if pd.isna(people_text):
        preds.append({"predicted_label": None, "score": None})
        people_entities.append(None)
    else:
        doc_people = nlp_people(str(people_text))

        # classification
        if doc_people.cats:
            label = max(doc_people.cats, key=doc_people.cats.get)
            score = doc_people.cats[label]
        else:
            label = None
            score = None

        preds.append({"predicted_label": label, "score": score})

        # PERSON entities
        persons = [ent.text for ent in doc_people.ents if ent.label_ == "PERSON"]
        people_entities.append("|".join(persons) if persons else None)

    # ========== SPACE MODEL on df["text"] ==========
    space_text = row["text"]

    if pd.isna(space_text):
        space_entities.append(None)
    else:
        doc_space = nlp_space(str(space_text))
        spaces = [ent.text for ent in doc_space.ents if ent.label_ in ["GPE", "LOC"]]
        space_entities.append("|".join(spaces) if spaces else None)

# -----------------------------
# 4. Add new columns
# -----------------------------
pred_df = pd.DataFrame(preds)
df = pd.concat([df, pred_df], axis=1)

df["people_extracted"] = people_entities
df["space_extracted"] = space_entities

# -----------------------------
# 5. Save output
# -----------------------------
output_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_3_running_the_model_to_extract_social_groups/sample_1870_1920_with_predictions.csv"
df.to_csv(output_path, index=False)

print(f"Predictions saved to {output_path}")
