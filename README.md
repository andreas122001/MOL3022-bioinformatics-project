# MOL3022-bioinformatics-project

This repository is related to a project in the course *MOL3022 Bioinformatics - Method Oriented Project* and contains the code for the backend application and for training and testing the machine learning model.

The model training and testing can be found in the notebooks `training.ipynb` and `testing.ipynb`, respectively.

The frontend code can be found at https://github.com/Senja20/mol-3022-front-end-application.

The model card for the machine learning model can be found at https://huggingface.co/andreas122001/mol3022-signal-peptide-prediction.


## Data format

The program expects data to be in FASTA format with a header where the kingdom (organism group) is at the first index of the header, and the kingdom is one "EUKARYA", "ARCHAEA", "POSITIVE" or "NEGATIVE". For example:

```
>EUKARYA|other_header_items
MSGYSPLSSGPADVHIGKAGFFSSVINLANTILGAGILSLPNAFTKTGLLFGCLTIVFSAFASFLGLYFV
```

Example data in the correct format is provided in `data/examples_small.fasta` and `data/examples.fasta`. 


## Usage

### Requirements
This project assumes you have Python installed on your machine.

To install requirements, do:

```bash
pip install -r requirements.txt
```

Run it either by (1) hosting the backend-frontend servers, or (2) by running the CLI:

### (1) Host the backend

To run the backend:

```bash
python src/api.py
```

This will automatically download the machine learning model, if it is not already on your machine, and run it on the backend server.

See [frontend repo](https://github.com/Senja20/mol-3022-front-end-application) for instructions on how to run the frontend.

### (2) Run as CLI

Alternatively, run the CLI like this:
```bash
python src/cli.py --file path/to/file.fasta
```
```bash
# E.g. test it on the example file like this:
python src/cli.py --file data/examples_small.fasta
```

This will also automatically download the machine learning model, but will only run it on the provided dataset. You can test it out using the example data.

You can also see the video guide:

https://github.com/andreas122001/MOL3022-bioinformatics-project/assets/70771608/e2964160-7a9d-4e27-bdd5-b655587ee75c

Usage of the CLI can be seen below:

```txt
usage: sp_predict [-h] -f FILE [-o OUTPUT] [-b BATCH_SIZE] [-v | --verbose | --no-verbose] [-t THRESHOLD]

Predicts if a protein sequence has a signal peptide or not. It writes a .fasta file, and adds a header to it with the
prediction and outputs it.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The path of the file you want to predict from.
  -o OUTPUT, --output OUTPUT
                        The path to the output file.
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        Batch size used for prediction. Default is 8. If prediction is very slow or fails, try
                        lowering it.
  -v, --verbose, --no-verbose
                        Shows progress bar and outputs SPs when writing to file. Default is not verbose.
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold for prediction. Prediction confidence must be over threshold to be considered
                        positive. Default is 90% confidence.
```

