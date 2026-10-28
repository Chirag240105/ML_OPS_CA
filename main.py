
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pathlib import Path
import pandas as pd
import joblib

app = FastAPI(
    title="Heart Disease Prediction API",
    description="ML prediction API using a trained Scikit-learn pipeline",
)


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "heart_model.pkl"
)

model = joblib.load(MODEL_PATH)


class HeartInput(BaseModel):
    Age: int = Field(ge=1, le=120)
    Sex: str
    ChestPainType: str
    RestingBP: float = Field(ge=0)
    Cholesterol: float = Field(ge=0)
    FastingBS: int = Field(ge=0, le=1)
    RestingECG: str
    MaxHR: int = Field(ge=0, le=250)
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str


@app.get("/")
def home():
    return {
        "message": "Heart Disease Prediction API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: HeartInput):
    input_df = pd.DataFrame([data.model_dump()])

    prediction = int(model.predict(input_df)[0])
    print("Prediction:", model.predict(input_df))
    print("Classes:", model.classes_)
    print("Probabilities:", model.predict_proba(input_df))

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(
            model.predict_proba(input_df)[0][1]
        )

    return {
        "prediction": prediction,
        "label": (
            "Heart disease indicated by the model"
            if prediction == 1
            else "No heart disease indicated by the model"
        ),
        "class_1_probability": probability,
        "note": "Educational demonstration only; not a medical diagnosis."
    }

    
