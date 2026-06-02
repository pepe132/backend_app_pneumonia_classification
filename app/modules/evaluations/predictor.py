import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "modelo_neumonia_app.pkl")


package = joblib.load(MODEL_PATH)

model = package["model"]
features = package["features"]
threshold_alto = package["threshold_alto"]
threshold_medio = package["threshold_medio"]
target_names = package["target_names"]


def predict_tabular_severity(evaluation_data):
    data = evaluation_data.model_dump()

    # Convierte booleanos True/False a 1/0
    for key, value in data.items():
        if isinstance(value, bool):
            data[key] = 1 if value else 0

    # Crear DataFrame
    x_eval = pd.DataFrame([data])

    missing_features = [feature for feature in features if feature not in x_eval.columns]

    if missing_features:
        raise ValueError(f"Faltan columnas requeridas por el modelo: {missing_features}")

    # Mantener solo las columnas que usó el modelo
    x_eval = x_eval[features]

    # Probabilidades
    probs = model.predict_proba(x_eval)[0]

    # Decisión usando thresholds
    pred_final = 0

    if probs[1] >= threshold_medio:
        pred_final = 1

    if probs[2] >= threshold_alto:
        pred_final = 2

    severity = target_names[pred_final]

    return {
        "severity_tabular": severity,
        "prob_low": round(float(probs[0]), 4),
        "prob_medium": round(float(probs[1]), 4),
        "prob_high": round(float(probs[2]), 4),
    }