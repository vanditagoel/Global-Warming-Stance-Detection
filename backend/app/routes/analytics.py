import pandas as pd
from fastapi import APIRouter
from ..config import DATASET_PATH
from ..database import connection

router = APIRouter()

@router.get("/analytics")
def analytics():
    dataset = {"available": False}
    if DATASET_PATH.exists():
        df = pd.read_csv(DATASET_PATH, keep_default_na=False)
        labels = df["stance_label"].astype(str).str.strip()
        valid = labels.isin(["Favour","Against","None"])
        dataset = {
            "available": True, "total_records": int(len(df)),
            "labelled_records": int(valid.sum()), "unlabelled_records": int((~valid).sum()),
            "origin": df["data_origin"].value_counts().to_dict() if "data_origin" in df else {},
            "languages": df["detected_language"].value_counts().to_dict() if "detected_language" in df else {},
            "classes": labels[valid].value_counts().to_dict()
        }
    with connection() as con:
        predictions = con.execute("SELECT COUNT(*) AS n FROM predictions").fetchone()["n"]
        feedback = con.execute("SELECT COUNT(*) AS n FROM feedback").fetchone()["n"]
    return {"dataset": dataset, "prediction_count": predictions, "feedback_count": feedback}

@router.get("/history")
def history(limit: int = 100):
    limit = max(1, min(limit, 500))
    with connection() as con:
        rows = con.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return {"history": [dict(r) for r in rows]}
