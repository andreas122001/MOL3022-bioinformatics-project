"""
The main api
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict

from fastapi import FastAPI
from transformers.tokenization_utils_base import BatchEncoding

from classes import FastaData
from utils import init_app, init_model, not_completed

CLASSIFIER, TOKENIZER = init_model()

app: FastAPI = init_app()

pool = ProcessPoolExecutor(max_workers=1, initializer=init_model)


async def model_predict(data: Dict) -> Dict[float, float]:
    r"""
    Predicts the probabilities of two classes using a pre-trained classifier model.

    Args:
        data (Dict): A dictionary containing the input data for prediction.

    Returns:
        Dict[float, float]: A dictionary containing the predicted probabilities for each class.
            The keys represent the class labels, and the values represent
            the corresponding probabilities.
    """
    global CLASSIFIER

    prediction = CLASSIFIER(**data).logits.flatten().softmax(-1).cpu().detach().numpy()

    return {"no_sp": prediction[0].item(), "sp": prediction[1].item()}


def preprocess(data) -> BatchEncoding:
    r"""
    Preprocesses the input data by tokenizing the kingdom and sequence.

    Args:
        data: The input data containing the header and sequence.

    Returns:
        The tokenized features as a BatchEncoding object.
    """

    global TOKENIZER

    # >EUKARYA|SJWUS12|sad2|w82

    # TODO: auto-find kingdom or enforce idx 0
    kingdom = data.header[1:].split("|")[0]
    sequence = data.sequence

    feats: str = (
        " ".join(list(kingdom)) + " [SEP] " + " ".join(list(sequence))
    )
    tokenized_feats: BatchEncoding = TOKENIZER(feats, return_tensors="pt")

    return tokenized_feats


@app.post("/inference")
async def post_inference(request: FastaData) -> Dict:
    r"""
    Perform inference on the given FASTA data.

    Args:
        request (FastaData): The FASTA data to perform inference on.

    Returns:
        Dict: A dictionary containing the inference results.
    """
    print(request)

    tokenized_data: BatchEncoding = preprocess(request)

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    result: Dict[float, float] = await loop.create_task(
        coro=model_predict(data=tokenized_data)
    )

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)

