from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os, pandas as pd

app = FastAPI(title="Loan Approval Predictor - Backend")

MODEL_PATH = os.environ.get("MODEL_PATH", "model/loan_model.pkl")

class LoanApplication(BaseModel):
    Gender: str | None = None
    Married: str | None = None
    Dependents: str | None = None
    Education: str | None = None
    Self_Employed: str | None = None
    ApplicantIncome: float | None = None
    CoapplicantIncome: float | None = None
    LoanAmount: float | None = None
    Loan_Amount_Term: float | None = None
    Credit_History: float | None = None
    Property_Area: str | None = None

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
