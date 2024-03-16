"""
The main api
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict, LiteralString

from fastapi import FastAPI
from transformers.tokenization_utils_base import BatchEncoding

from classes import FastaData
from utils import init_app, init_model, not_completed

CLASSIFIER, TOKENIZER = init_model()

app: FastAPI = init_app()

pool = ProcessPoolExecutor(max_workers=1, initializer=init_model)


async def model_predict(data: Dict) -> Dict[float, float]:
    """
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


@app.get("/hello")
def hello_world() -> Dict[str, str]:
    """
    A function that prints "Hello, World!" and returns a dictionary with a message.
    This for debugging purposes.

    Returns:
        dict: A dictionary with a single key "message" and value "Hello, World!".
    """
    print("Hello, World!")
    return {"message": "Hello, World!"}


def preprocess(data) -> BatchEncoding:
    """
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

    feats: LiteralString = (
        " ".join(list(kingdom)) + " [SEP] " + " ".join(list(sequence))
    )
    tokenized_feats: BatchEncoding = TOKENIZER(feats, return_tensors="pt")

    return tokenized_feats


@app.post("/inference")
async def post_inference(request: FastaData) -> Dict:
    """
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


@not_completed
class BatchScheduler:
    """
    A class that manages batch scheduling of tasks.

    Attributes:
        tasks (list): A list of tasks to be processed.
        max_tasks (int): The maximum number of tasks that can be added to the scheduler.
        should_run (bool): Indicates whether the scheduler should start running the tasks.
        processor (function): The function used to process the tasks.

    Methods:
        run_tasks(): Runs the tasks using the processor function.
        add_task(task: Any): Adds a task to the scheduler.

    """

    tasks = []
    max_tasks = 8
    should_run = False
    processor = lambda x: x  # TODO: remove the lambda and add the actual function

    def run_tasks(self):
        """
        Executes the tasks using the processor.

        This method executes the tasks stored in the `tasks` attribute using the `processor` method.
        """
        self.processor(self.tasks)

    def add_task(self, task: Any):
        """
        Add a task to the task list.

        Parameters:
        - task (Any): The task to be added.

        Returns:
        None
        """
        if len(self.tasks) >= self.max_tasks:
            self.should_run = True
        self.tasks.append(task)
