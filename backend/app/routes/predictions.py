import json
from fastapi import APIRouter, HTTPException
from ..schemas import PredictRequest, BatchRequest, FeedbackRequest
from ..database import connection
from ..config import LABELS
from ..services.model_service import model_service, guess_language

router = APIRouter()

def run_prediction(text):
    try:
        label, scores = model_service.predict_one(text)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    lang = guess_language(text)
    with connection() as con:
        cur = con.execute(
            "INSERT INTO predictions(text,predicted_label,scores_json,language,model_name) VALUES(?,?,?,?,?)",
            (text, label, json.dumps(scores), lang, model_service.model_name)
        )
        pid = cur.lastrowid
    return {"id": pid, "text": text, "predicted_label": label, "scores": scores,
            "detected_language": lang, "model_name": model_service.model_name,
            "score_note": "Relative normalized decision scores; not calibrated probabilities."}

@router.post("/predict")
def predict(req: PredictRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="Comment cannot be blank.")
    return run_prediction(req.text.strip())

@router.post("/predict/batch")
def predict_batch(req: BatchRequest):
    if any(not isinstance(t, str) or not t.strip() for t in req.texts):
        raise HTTPException(status_code=422, detail="Every comment must be non-empty.")
    return {"results": [run_prediction(t.strip()) for t in req.texts]}

@router.post("/explain")
def explain(req: PredictRequest):
    if model_service.pipeline is None:
        raise HTTPException(status_code=503, detail="Train the model first.")
    label, scores = model_service.predict_one(req.text)
    pipe = model_service.pipeline
    features = pipe.named_steps["features"]
    clf = pipe.named_steps["classifier"]
    x = features.transform([req.text])
    names = features.get_feature_names_out()
    # Explain using signed linear contributions for the predicted class.
    class_idx = list(clf.classes_).index(label)
    coef = clf.coef_[class_idx] if len(clf.classes_) > 2 else clf.coef_[0] * (1 if label == clf.classes_[1] else -1)
    row = x.tocoo()
    contributions = [(str(names[i]), float(v * coef[i])) for i, v in zip(row.col, row.data)]
    contributions.sort(key=lambda z: abs(z[1]), reverse=True)
    return {"predicted_label": label, "top_features": [{"feature": f, "contribution": c} for f,c in contributions[:10]],
            "note": "Feature contributions are model diagnostics, not causal explanations."}

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    if req.corrected_label not in LABELS:
        raise HTTPException(status_code=422, detail=f"corrected_label must be one of {LABELS}")
    with connection() as con:
        cur = con.execute(
            "INSERT INTO feedback(prediction_id,text,predicted_label,corrected_label) VALUES(?,?,?,?)",
            (req.prediction_id, req.text, req.predicted_label, req.corrected_label)
        )
        return {"status": "saved", "feedback_id": cur.lastrowid,
                "message": "Feedback stored separately; it is not automatically added to training data."}
