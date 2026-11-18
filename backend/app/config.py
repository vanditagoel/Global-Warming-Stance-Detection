import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(os.getenv("MODEL_PATH", ROOT / "models/baseline_pipeline.joblib"))
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", ROOT / "backend/app/stance_history.db"))
DATASET_PATH = Path(os.getenv("DATASET_PATH", ROOT / "data/raw/Indic_Climate_Stance_Expanded_1806.csv"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
LABELS = ["Favour", "Against", "None"]
