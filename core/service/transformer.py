# Use a pipeline as a high-level helper
# from transformers import pipeline
import requests
from config.settings import COMMON, HuggingFace

# import torch
import sys
import os

API_URL = "https://api-inference.huggingface.co/models/"
headers = {"Authorization": "Bearer " + HuggingFace.API_KEY}


class Transformer:
    def __init__(self, model):
        self.model = model
        self.pipe = None

    def query(self, payload):
        response = requests.post(API_URL + self.model, headers=headers, json=payload)
        return response.json()

    def load_model(self):
        pass
        # commandline_args = os.environ.get('COMMANDLINE_ARGS', "--skip-torch-cuda-test --no-half")
        # sys.argv += commandline_args
        # self.pipe = pipeline(
        #     "text-classification",
        #     model=self.model,
        #     device="cpu",
        #     return_all_scores=True,
        #     torch_dtype=torch.float16,
        # )
        # self.pipe.enable_model_cpu_offload()

    def predict(self, text):
        if COMMON.is_local and self.pipe is None:
            self.load_model()

        if COMMON.is_local:
            return self.pipe(text)
        else:
            return self.query({"inputs": text})


# transformer_model = Transformer("ProsusAI/finbert")
transformer_model = Transformer("bert-base-cased")


def predicts(text: [str]):
    result = transformer_model.pipe(text)
    return result


def predict(text: str):
    result = transformer_model.predict(text)
    return result
