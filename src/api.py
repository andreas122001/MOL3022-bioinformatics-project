from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Any, List, Dict
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from concurrent.futures import ProcessPoolExecutor

_threshold = 0.7
_classifier = None
_tokenizer = None


class FastaData(BaseModel):
    header: str
    sequence: str
    # threshold: float = _threshold

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_model():
    global _classifier, _tokenizer
    _classifier = AutoModelForSequenceClassification.from_pretrained("andreas122001/mol3022-signal-peptide-prediction")
    _tokenizer = AutoTokenizer.from_pretrained("andreas122001/mol3022-signal-peptide-prediction")
    print("MODEL INITIALIZED")

init_model()


pool = ProcessPoolExecutor(max_workers=1, initializer=init_model)


async def model_predict(data: Dict) -> Dict[float,float]:
    global _classifier

    prediction = _classifier(**data) \
                    .logits \
                    .flatten() \
                    .softmax(-1) \
                    .cpu() \
                    .detach() \
                    .numpy()

    return {
        'no_sp': prediction[0].item(),
        'sp'   : prediction[1].item()
    }

@app.get("/hello")
def hello_world():
    print("Hello, World!")
    return {
        "message": "Hello, World!"
    }

def preprocess(data):
    global _tokenizer

    # TODO: auto-find kingdom or enforce idx 0
    kingdom = data.header[1:].split("|")[0]
    sequence = data.sequence

    feats = " ".join(list(kingdom)) + " [SEP] " + " ".join(list(sequence))
    tokenized_feats = _tokenizer(feats, return_tensors="pt")

    return tokenized_feats



@app.post("/inference")
async def post_inference(request: FastaData) -> Dict:
    print(request)

    tokenized_data = preprocess(request)

    loop = asyncio.get_event_loop()
    result = await loop.create_task(model_predict(tokenized_data))


    return result


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, port=8080)




class BatchScheduler:
    tasks = []
    max_tasks = 8
    should_run = False
    processor = None

    def run_tasks(self):
        self.processor(self.tasks)

    def add_task(self, task: Any):
        if len(self.tasks) >= self.max_tasks:
            self.should_run = True
        self.tasks.append(task)
        
        