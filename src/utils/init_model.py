"""
Module for the function which initializes the model and tokenizer for signal peptide prediction.
"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer


def init_model():
    """
    Initializes the model and tokenizer for signal peptide prediction.

    Returns:
        classifier (AutoModelForSequenceClassification):
        The pre-trained model for sequence classification.
        tokenizer (AutoTokenizer): The tokenizer for tokenizing input sequences.
    """
    classifier = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path="andreas122001/mol3022-signal-peptide-prediction"
    )
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path="andreas122001/mol3022-signal-peptide-prediction"
    )

    return classifier, tokenizer
