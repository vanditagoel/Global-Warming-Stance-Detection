from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import CORS_ORIGINS
from .database import init_db
from .services.model_service import model_service
from .routes import predictions, analytics

app = FastAPI(title="Indic Climate Stance Challenge API", version="1.0.0",
              description="Hindi and Bengali climate stance classification API.")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(predictions.router, tags=["Predictions"])
app.include_router(analytics.router, tags=["Analytics"])

@app.on_event("startup")
def startup():
    init_db()
    model_service.load()

@app.get("/")
def root():
    return {"project": "Indic Climate Stance Challenge", "status": "running",
            "classes": ["Favour", "Against", "None"]}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_service.pipeline is not None,
            "model_name": model_service.model_name}
