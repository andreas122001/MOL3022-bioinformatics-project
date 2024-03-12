from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModel
from typing import List, Dict
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from concurrent.futures import ProcessPoolExecutor

_threshold = 0.7
_model = None


class FastaData(BaseModel):
    header: str
    sequence: str
    threshold: float = _threshold

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
    global _model
    _model = None
    # model = AutoModel.from_pretrained(...)

# pool = ProcessPoolExecutor(max_workers=1, initializer=init_model)


async def model_predict(header: str, sequence: str) -> Dict[float,float]:
    await asyncio.sleep(3.)
    return {
        'no_sp': 0.2,
        'sp': 0.8,
    }

@app.get("/hello")
def hello_world():
    print("Hello, World!")
    return {
        "message": "Hello, World!"
    }

@app.post("/inference")
async def post_inference(data: FastaData):
    print(data)

    result = await model_predict(data.header, data.sequence)

    return {
        'positive': result['sp'],
        'negative': result['no_sp'],
        'predicted': 'Signal peptide' if result['sp'] > data.threshold
            else 'No signal peptide' if result['no_sp'] > data.threshold
            else 'Uncertain'
    }


