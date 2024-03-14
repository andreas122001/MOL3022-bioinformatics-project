
### PARSE ARGUMENTS ###
import argparse

parser = argparse.ArgumentParser(
    prog="sp_predict",
    description="Predicts if a protein sequence has a singal peptide or not. It writes a .fasta file, adds a header to it with the prediction and outputs it."
)
parser.add_argument("-f", "--file", help="The file you want to predict", type=str, required=True)
parser.add_argument("-o", "--output", help="The output file", type=str)
parser.add_argument("-b", "--batch_size", help="Batch size used for prediction", default=8, type=int)
parser.add_argument("-v", "--verbose", help="Print everything or not", default=True, type=bool)
parser.add_argument("-t", "--threshold", help=f"Threshold for prediction. Prediction confidence must be over threshold to be considered positive. Default is 95%% confidence", default=0.95, type=float)
args = parser.parse_args()


data = None
with open(args.file, "r") as f:
    data = f.read()
    data = data.split(">")
    data = [d for d in data if d]

    formatted_data = []
    for d in data:
        header, sequence = d.split("\n")[:2]
        kingdom = header.split("|")[0]
        legal_kingdoms = ["EUKARYA", "ARCHAEA", "POSITIVE", "NEGATIVE"]
        if kingdom not in legal_kingdoms:
            raise ValueError(
                f""" \
                Expected header value at index 0 to be one of {legal_kingdoms}.
                """
            )
        formatted_data.append({
            'kingdom': kingdom,
            'sequence': sequence
        })
    data = formatted_data


### PREPROCESSING ###
from transformers import AutoTokenizer

MODEL_PATH = "andreas122001/mol3022-signal-peptide-prediction"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def preprocess(data):
    global tokenizer

    kingdom = data['kingdom']
    sequence = data['sequence']

    feats = " ".join(list(kingdom)) + " [SEP] " + " ".join(list(sequence))
    tokenized_feats = tokenizer(feats, return_tensors="pt")
    tokenized_feats = {k: v.flatten() for k, v in tokenized_feats.items()}

    tokenized_feats['kingdom'] = data['kingdom']
    tokenized_feats['sequence'] = data['sequence']

    return tokenized_feats

tokenized_data = [preprocess(d) for d in data]


### PREDICT ###
from transformers import AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
batches = torch.utils.data.DataLoader(tokenized_data, batch_size=args.batch_size)

for batch in batches:

    preds = model(
                    input_ids=batch['input_ids'],
                    attention_mask=batch['attention_mask']
                ).logits \
                .softmax(-1) \
                .cpu() \
                .detach() \
                .numpy()
    
    preds = ['SP' if pred[1] > args.threshold else 'NO_SP' for pred in preds]

    for pred, kingdom, seq in zip(preds, batch['kingdom'], batch['sequence']):
        msg = f">{kingdom}|{pred}\n{seq}\n"
        if args.output:
            with open(args.output, "a") as f:
                f.write(msg)
        else:
            print(msg, end="")
