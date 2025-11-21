import spacy
from spacy.tokens import DocBin
import pandas as pd
import random
from pathlib import Path

# -----------------------------
# 1. Load labeled CSV
# -----------------------------
# Columns:
#   entity -> text to classify
#   label  -> social group (aristocracy / clergy / public officials / royals)
annotations = pd.read_csv(
    "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/entity_labels_2025-11-20.csv"
)

# -----------------------------
# 2. Convert CSV rows into spaCy textcat examples
# -----------------------------
def csv_to_textcat_examples(df):
    examples = []
    for _, row in df.iterrows():
        text = row["entity"]  # <- use entity column
        label = row["label"]
        examples.append({"text": text, "cats": {label: 1}})
    return examples

examples = csv_to_textcat_examples(annotations)

# -----------------------------
# 3. Split into train/dev
# -----------------------------
random.seed(42)
random.shuffle(examples)
split = int(len(examples) * 0.8)
train_data = examples[:split]
dev_data = examples[split:]

# -----------------------------
# 4. Convert to DocBin (.spacy)
# -----------------------------
def create_textcat_docbin(data, nlp, labels):
    doc_bin = DocBin()
    for item in data:
        doc = nlp.make_doc(item["text"])
        # initialize all labels to 0
        doc.cats = {label: 0.0 for label in labels}
        # set positive label
        for label in item["cats"]:
            doc.cats[label] = 1.0
        doc_bin.add(doc)
    return doc_bin

LABELS = ["aristocracy", "clergy", "public officials", "royals"]

nlp = spacy.blank("en")
textcat = nlp.add_pipe("textcat")  # exclusive classes (one label per text)
for label in LABELS:
    textcat.add_label(label)

train_docbin = create_textcat_docbin(train_data, nlp, LABELS)
dev_docbin   = create_textcat_docbin(dev_data, nlp, LABELS)

# -----------------------------
# 5. Define clear paths for saving
# -----------------------------
train_path = Path("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/train/train.spacy")
dev_path   = Path("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/dev/dev.spacy")

# Make sure directories exist
train_path.parent.mkdir(parents=True, exist_ok=True)
dev_path.parent.mkdir(parents=True, exist_ok=True)

# Save DocBin
train_docbin.to_disk(train_path)
dev_docbin.to_disk(dev_path)

print(f"Saved train data to {train_path}")
print(f"Saved dev data to {dev_path}")

# -----------------------------
# 6. Train model (in terminal)
# -----------------------------
# 1) Initialize config.cfg
# python -m spacy init config config.cfg --lang en --pipeline textcat --force
#
# 2) Train the model
#python -m spacy train config.cfg \
#    --output "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/model" \
#    --paths.train "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/train/train.spacy" \
#    --paths.dev "/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_3/Activity_2_text_classification_model/spacy_training/dev/dev.spacy"


acy --paths.dev dev/dev.spacy
