from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

class BatchRequest(BaseModel):
    texts: List[str] = Field(min_length=1, max_length=200)

class FeedbackRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    predicted_label: Optional[str] = None
    corrected_label: str
    prediction_id: Optional[int] = None

class PredictionResponse(BaseModel):
    text: str
    predicted_label: str
    scores: Dict[str, float]
    detected_language: str
    model_name: str
    score_note: str
