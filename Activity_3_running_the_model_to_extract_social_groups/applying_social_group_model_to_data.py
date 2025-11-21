import spacy
import pandas as pd

# -----------------------------
# 1. Load your trained text classification model
# Make sure to point to model-best, not just the output folder
# -----------------------------



model_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/model/model-best"
nlp = spacy.load(model_path)

# -----------------------------
# 2. Load the dataset you want to classify
# -----------------------------
data_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/sample_1870_1920_long_tailored_entities.csv"
df = pd.read_csv(data_path)

# -----------------------------
# 3. Apply the model to the `tailored_entities` column
# -----------------------------
preds = []
for text in df["People"]:
    if pd.isna(text):
        preds.append({"predicted_label": None, "score": None})
        continue

    text = str(text)  # ensure input is a string
    doc = nlp(text)
    label = max(doc.cats, key=doc.cats.get)  # get label with highest score
    score = doc.cats[label]
    preds.append({"predicted_label": label, "score": score})

# -----------------------------
# 4. Add predictions to the dataframe
# -----------------------------
pred_df = pd.DataFrame(preds)
df = pd.concat([df, pred_df], axis=1)

# -----------------------------
# 5. Save the results
# -----------------------------
output_path = "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_3_running_the_model_to_extract_social_groups/sample_1870_1920_with_predictions.csv"
df.to_csv(output_path, index=False)

print(f"Predictions saved to {output_path}")
