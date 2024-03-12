from torch.utils.data import Dataset
from typing import Any
from tqdm import tqdm
import pandas as pd
from abc import abstractmethod

def load_data(path):
    ds = []
    # Read from src
    with open(path) as f:
        lines = f.read().split(">")[1:]
        ds = [0]*len(lines)
        for i, line in enumerate(tqdm(lines)):
            header, seq, sep = line.strip().split("\n")
            seq = " ".join(seq)
            ac, kingdom, type_ = header.split("|")[:3]
            ds[i] = {
                'text': seq,
                'labels': sep,
                'uniprot_ac': ac,
                'kingdom': kingdom,
                'type': type_,
            }
    return ds

class AbstractFastaDataset(Dataset):
    def __getitem__(self, index) -> Any:
        return self.data[index]
    
    def __len__(self):
        return len(self.data)
    
class SPFastaDataset(AbstractFastaDataset):
    def __init__(self, path) -> None:
        data = load_data(path)
        self.data = pd.DataFrame(data)

class SPFastaDatasetBinary(AbstractFastaDataset):
    def __init__(self, path) -> None:
        data = load_data(path)
        for x in tqdm(data):
            x['labels'] = 0 if x['type'] == 'NO_SP' else 1
        self.data = pd.DataFrame(data)

class SPFastaDatasetMultiLabel(AbstractFastaDataset):
    label2id = {
        'NO_SP': 0, 
        'SP': 1,
        'LIPO': 2,
        'TAT': 3,
        'TATLIPO': 4,
        'PILIN': 5,
    }
    def __init__(self, path) -> None:
        data = load_data(path)
        for x in tqdm(data):
            x['labels'] = self.label2id[x['type']]
        self.data = pd.DataFrame(data)

class SPFastaDatasetBinaryWithTokenizedCategory(AbstractFastaDataset):
    def __init__(self, path) -> None:
        data = load_data(path)
        for x in tqdm(data):
            x['labels'] = 0 if x['type'] == 'NO_SP' else 1
            x['text'] = " ".join(x['kingdom']) + " [SEP] " + x['text']
        self.data = pd.DataFrame(data)