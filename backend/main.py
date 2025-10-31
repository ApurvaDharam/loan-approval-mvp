from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import joblib, os, pandas as pd

app = FastAPI(title="Loan Approval Predictor - Backend")

MODEL_PATH = os.environ.get("MODEL_PATH", "model/loan_model.pkl")

class LoanApplication(BaseModel):
    Gender: Optional[str] = None
    Married: Optional[str] = None
    Dependents: Optional[str] = None
    Education: Optional[str] = None
    Self_Employed: Optional[str] = None
    ApplicantIncome: Optional[float] = None
    CoapplicantIncome: Optional[float] = None
    LoanAmount: Optional[float] = None
    Loan_Amount_Term: Optional[float] = None
    Credit_History: Optional[float] = None
    Property_Area: Optional[str] = None

model = None

@app.on_event('startup')
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        # lazy warning - in CI we may not have model file
        model = None

@app.get('/health')
def health():
    return {'status': 'ok', 'model_loaded': model is not None}

@app.post('/predict')
def predict(payload: LoanApplication):
    if model is None:
        return {'error': 'model not found. Train model and save to backend/model/loan_model.pkl'}
    data = payload.dict()
    df = pd.DataFrame([data])
    # The model pipeline used in the notebook expects certain columns; missing ones are fine (imputer in pipeline)
    proba = float(model.predict_proba(df)[:,1][0])
    pred = int(model.predict(df)[0])
    return {'approved': 'Yes' if pred==1 else 'No', 'score': proba}
