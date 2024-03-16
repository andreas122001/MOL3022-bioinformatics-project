"""
Model for the FastaData class
"""

from pydantic import BaseModel


class FastaData(BaseModel):
    """
    Represents a FASTA data object.

    Attributes:
        header (str): The header of the FASTA sequence.
        sequence (str): The sequence data in the FASTA format.
    """

    header: str
    sequence: str
