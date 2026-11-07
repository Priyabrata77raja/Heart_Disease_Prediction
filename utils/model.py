"""Loads the user's real trained model/pipeline. Never fabricates a model."""
from pathlib import Path
import pickle

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXTS = {".pkl", ".pickle", ".joblib", ".sav"}
# Exact column names/categories of the common Heart Failure Prediction dataset
FEATURES = ["Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", "FastingBS",
            "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"]


def find_model_file():
    for folder in (ROOT / "models", ROOT):
        if folder.exists():
            for p in sorted(folder.iterdir()):
                if p.suffix.lower() in EXTS and p.is_file():
                    return p
    return None


def load_model():
    """Returns (model, filename, error_message)."""
    path = find_model_file()
    if path is None:
        return None, None, "No trained model file found. Put your .pkl/.joblib file in the models/ folder."
    try:
        try:
            import joblib
            return joblib.load(path), path.name, None
        except Exception:
            with open(path, "rb") as f:
                return pickle.load(f), path.name, None
    except Exception as exc:  # noqa: BLE001
        return None, path.name, f"Could not load {path.name}: {exc}"


def predict(model, values: dict):
    """Run the real model. Raises on any mismatch so the UI can explain it."""
    row = pd.DataFrame([values])[FEATURES]
    expected = getattr(model, "feature_names_in_", None)
    if expected is not None and set(expected) == set(row.columns):
        row = row[list(expected)]
    pred = model.predict(row)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(row)[0]
    classes = getattr(model, "classes_", None)
    return row, pred, proba, classes


def is_positive(pred):
    try:
        return int(pred) == 1
    except (TypeError, ValueError):
        return str(pred).strip().lower() in {"yes", "true", "positive", "heart disease"}
