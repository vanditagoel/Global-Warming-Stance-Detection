import joblib
import numpy as np
from pathlib import Path
from ..config import MODEL_PATH, LABELS

class ModelService:
    def __init__(self):
        self.pipeline = None
        self.model_name = "TF-IDF word+character / LinearSVC"

    def load(self):
        if Path(MODEL_PATH).exists():
            self.pipeline = joblib.load(MODEL_PATH)
        return self.pipeline is not None

    def predict_one(self, text: str):
        if self.pipeline is None:
            raise RuntimeError("Model is not trained. Run: python ml/train_baseline.py")
        pred = str(self.pipeline.predict([text])[0])
        estimator = self.pipeline.named_steps["classifier"]
        vectorizer = self.pipeline.named_steps["features"]
        transformed = vectorizer.transform([text])
        decision = estimator.decision_function(transformed)
        if decision.ndim == 1:
            decision = np.column_stack([-decision, decision])
        # Normalized decision scores are for relative visualization only, not calibrated probabilities.
        shifted = decision[0] - np.max(decision[0])
        exp = np.exp(shifted)
        vals = exp / exp.sum()
        classes = list(estimator.classes_)
        scores = {label: float(vals[classes.index(label)]) if label in classes else 0.0 for label in LABELS}
        return pred, scores

model_service = ModelService()

def guess_language(text: str) -> str:
    has_deva = any("\u0900" <= c <= "\u097f" for c in text)
    has_beng = any("\u0980" <= c <= "\u09ff" for c in text)
    if has_deva and has_beng: return "mixed-script"
    if has_deva: return "Hindi-script (heuristic)"
    if has_beng: return "Bengali-script (heuristic)"
    return "Latin/Romanised/English (uncertain)"
