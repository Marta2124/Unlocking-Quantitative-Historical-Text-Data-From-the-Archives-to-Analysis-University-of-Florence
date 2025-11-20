import spacy
from spacy.tokens import DocBin
import pandas as pd
import random
from pathlib import Path

# -----------------------------
# Load your labeled CSV
# -----------------------------
annotations = pd.read_csv("/Users/martapagnini/Library/CloudStorage/Dropbox/Marta 30_10_2024/Teaching/Workshop_Florence_11_25/Github/Session_2/Activity_4A_Creating_a_Tailored_Spacy_Model/output/annotations.csv")

# -----------------------------
# Convert CSV to spaCy JSONL-like data
# -----------------------------
def csv_to_examples(df):
    examples = []
    for text, group in df.groupby("text"):
        spans = []
        # Sort entities by start index
        for _, row in group.iterrows():
            start = text.find(row["entity"])
            if start == -1:
                continue
            end = start + len(row["entity"])
            label = row["label"]

            # Check for overlapping with existing spans
            overlap = False
            for s, e, _ in spans:
                if not (end <= s or start >= e):
                    overlap = True
                    break
            if not overlap:
                spans.append((start, end, label))

        if spans:
            examples.append({"text": text, "entities": spans})
    return examples

examples = csv_to_examples(annotations)

# -----------------------------
# Split into train/dev
# -----------------------------
random.seed(123)
random.shuffle(examples)
split = int(len(examples) * 0.8)
train_data = examples[:split]
dev_data = examples[split:]

# -----------------------------
#  Convert to DocBin (.spacy)
# -----------------------------
def create_docbin(data, nlp):
    doc_bin = DocBin()
    for item in data:
        doc = nlp.make_doc(item["text"])
        ents = []
        for start, end, label in item["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is not None:
                ents.append(span)
        doc.ents = ents
        doc_bin.add(doc)
    return doc_bin

nlp = spacy.blank("en")  # blank English model

train_docbin = create_docbin(train_data, nlp)
dev_docbin = create_docbin(dev_data, nlp)

Path("train").mkdir(exist_ok=True)
Path("dev").mkdir(exist_ok=True)

train_docbin.to_disk("train/train.spacy")
dev_docbin.to_disk("dev/dev.spacy")

# you'll see a dev and a train folder in your file
# -----------------------------
# Once having run code 1 to 79, train the NER model in the terminal
# -----------------------------
# From terminal:
# python -m spacy init config config.cfg --lang en --pipeline ner --optimize efficiency --force

# python -m spacy train config.cfg --output ./model --paths.train train/train.spacy --paths.dev dev/dev.spacy

# -----------------------------
#  Load and test the model
# -----------------------------
# if you find an error: No matching distribution found for smart-open <7.0.0
# conda create -n spacyenv python=3.10 -y
# conda activate spacyenv

# pip install -U pip setuptools wheel
# pip install spacy
# python -m spacy validate
# python -m spacy init config config.cfg --lang en --pipeline ner --optimize efficiency --force
# python -m spacy train config.cfg --output ./model --paths.train train/train.spacy --paths.dev dev/dev.spacy