import os
import sys
import logging

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from fastapi import FastAPI
from starlette.responses import JSONResponse

from predictor.predict import ModelPredictor
from models.models import Stroke

logging.basicConfig(filename='api_main.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(module)s:%(levelname)s:%(message)s')

app = FastAPI()

@app.get('/', status_code=200)
async def healthcheck():
    logging.info("Healthy was checked and ready to go!.")
    return 'Stroke classifier is all ready to go!'

@app.post('/predict_stroke')
def extract_name(stroke_features: Stroke):
    logging.debug('predictor:', predictor)
    predictor = ModelPredictor("models/logistic_regression_output.pkl")
    X = [stroke_features.age,
        stroke_features.hypertension,
        stroke_features.heart_disease,
        stroke_features.avg_glucose_level,
        stroke_features.bmi,
        stroke_features.age_nan,
        stroke_features.avg_glucose_level_nan,
        stroke_features.bmi_nan,
        stroke_features.hypertension,
        stroke_features.heart_disease,
        stroke_features.gender_Male,
        stroke_features.ever_married_Yes,
        stroke_features.work_type_Never_worked,
        stroke_features.work_type_Private,
        stroke_features.work_type_Self_employed,
        stroke_features.work_type_children,
        stroke_features.Residence_type_Urban,
        stroke_features.smoking_status_formerly_smoked,
        stroke_features.smoking_status_never_smoked,
        stroke_features.smoking_status_smokes]
    prediction = predictor.predict([X])
    logging.debug(f"Resultado predicción: {prediction}")
    logging.error(f"Resultado predicción: {prediction}")
    logging.info(f"Resultado predicción: {prediction}")
    return JSONResponse(f"Resultado predicción: {prediction}")
