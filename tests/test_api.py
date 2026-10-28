
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Valid sample input
VALID_INPUT = {
    "Age": 40,
    "Sex": "M",
    "ChestPainType": "ATA",
    "RestingBP": 130,
    "Cholesterol": 220,
    "FastingBS": 0,
    "RestingECG": "Normal",
    "MaxHR": 170,
    "ExerciseAngina": "N",
    "Oldpeak": 0.0,
    "ST_Slope": "Up"
}


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Heart Disease Prediction API is running"
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict():
    response = client.post("/predict", json=VALID_INPUT)

    assert response.status_code == 200

    body = response.json()

    assert body["prediction"] in [0, 1]
    assert body["label"] in [
        "Heart disease indicated by the model",
        "No heart disease indicated by the model"
    ]
    assert body["class_1_probability"] is None or (
        0 <= body["class_1_probability"] <= 1
    )
    assert "note" in body


def test_missing_required_field():
    invalid_input = VALID_INPUT.copy()
    invalid_input.pop("Age")

    response = client.post("/predict", json=invalid_input)

    assert response.status_code == 422


def test_invalid_age():
    invalid_input = VALID_INPUT.copy()
    invalid_input["Age"] = 150

    response = client.post("/predict", json=invalid_input)

    assert response.status_code == 422


def test_invalid_fasting_blood_sugar():
    invalid_input = VALID_INPUT.copy()
    invalid_input["FastingBS"] = 2

    response = client.post("/predict", json=invalid_input)

    assert response.status_code == 422
