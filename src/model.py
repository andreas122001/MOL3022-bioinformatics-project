from torch import nn
import torch
import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer

detected_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ProtBertSequenceClassification:

    def __init__(self, device: str=detected_device) -> None:
        self.device = device

        self.model = AutoModelForSequenceClassification.from_pretrained("Rostlab/prot_bert", num_labels=2, device=device)
        self.model.label2id = {
            'NO_SP': 0,
            'SP': 1
        }
        self.model.id2label= {
            0: 'NO_SP',
            1: 'SP'
        }
        self.tokenizer = AutoTokenizer("Rostlab/prot_bert", device=device)

    def forward(self, x):

        logits = self.model(x).logits
        return nn.functional.softmax(logits, dim=-1)



