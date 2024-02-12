import torch, re
import torch.utils.data as data_utils
from torch.utils.data import Dataset
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_data():
    ds = []
    # Read from src
    with open('data/train_set.fasta') as f:
        lines = f.read().split(">")[1:]
        ds = [0]*len(lines)
        for i, line in enumerate(tqdm(lines)):
            header, seq, sep = line.strip().split("\n")
            # sep = re.sub("S|T|L|P", "0", sep) # simplify to SP existance
            # sep = re.sub("I|M|O",   "1", sep) # simplify to SP non-existance
            ac, kingdom, type_, id_ = header.split("|")
            sep = 1. if type_=="SP" in sep else 0.
            ds[i] = {
                'header': {
                    'uniprot_ac': ac,
                    'kingdom': kingdom,
                    'type': type_,
                    'id': id_
                },
                'seq': seq,
                'sep': sep
            }
    return pd.DataFrame(ds)

class SPDatasetBinary(Dataset):
    def __init__(self, path) -> None:
        super().__init__()

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        x, y = 0, 0
        return x, y
