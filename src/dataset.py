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
                'sequence': seq,
                'label': sep,
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
            x['label'] = 0. if x['type'] == 'NO_SP' else 1.
        self.data = pd.DataFrame(data)

class SPFastaDatasetBinaryWithTokenizedCategory(AbstractFastaDataset):
    def __init__(self, path) -> None:
        data = load_data(path)
        for x in tqdm(data):
            x['label'] = 0. if x['type'] == 'NO_SP' else 1.
            x['sequence'] = " ".join(x['kingdom']) + " [SEP] " + x['sequence']
        self.data = pd.DataFrame(data)