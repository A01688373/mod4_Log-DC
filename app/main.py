import logging
import os
import sys
import requests

from fastapi import FastAPI, Body
from starlette.responses import JSONResponse

logging.basicConfig(filename='api_main.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s')

app = FastAPI()

# ML model prediction function using the prediction API request
def predict():

    url3 = "http://server.docker:8000/"

    response = requests.request("GET", url3)
    response = response.text
    return response


def predict_stroke(input):
    url3 = "http://server.docker:8000/predict_stroke"

    response = requests.post(url3, json=input)
    response = response.text
    return response


@app.get('/')
def read_root():
    logging.info("Stroke Model Front-end is ready to go!")
    return "Sroke Model Front-end is ready to go!"

@app.get("/healthcheck")
async def v1_healhcheck():
    url3 = "http://server.docker:8000/"

    response = requests.request("GET", url3)
    response = response.text
    logging.info(f"Stroke in progress... : {response}")
    return response

@app.post('/predict')
def predictor(payload: dict = Body(...)):
    logging.info("Prediction requested.")
    response = predict_stroke(payload)
    return {"response": response}