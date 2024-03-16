import pandas as pd
from torch.utils.data import Dataset
from tqdm import tqdm


def load_data():
    """
    The function to load the data from the file.
    """
    ds = []
    # Read from src
    with open("data/train_set.fasta") as f:
        lines = f.read().split(">")[1:]
        ds = [0] * len(lines)
        for i, line in enumerate(tqdm(lines)):
            header, seq, sep = line.strip().split("\n")
            # sep = re.sub("S|T|L|P", "0", sep) # simplify to SP existance
            # sep = re.sub("I|M|O",   "1", sep) # simplify to SP non-existance
            ac, kingdom, type_, id_ = header.split("|")
            sep = 1.0 if type_ == "SP" in sep else 0.0
            ds[i] = {
                "header": {
                    "uniprot_ac": ac,
                    "kingdom": kingdom,
                    "type": type_,
                    "id": id_,
                },
                "seq": seq,
                "sep": sep,
            }
    return pd.DataFrame(ds)


class SPDatasetBinary(Dataset):
    """
    Custom dataset class for the signal peptide prediction task.
    """

    def __init__(self, path) -> None:
        super().__init__()

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        x, y = 0, 0
        return x, y
