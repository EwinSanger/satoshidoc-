from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict
import os

app = FastAPI(title="SatoshiDoc Server", version="1.0.0")

DEFAULT_LANG = os.getenv("APP_LANG", "en")
DEFAULT_RISK = float(os.getenv("RISK_PERCENT", "0.02"))

class PredictIn(BaseModel):
    message: str
    context: Optional[Dict] = None

class PredictOut(BaseModel):
    reply: str
    meta: Optional[Dict] = None

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn = Body(...)):
    msg = payload.message.strip()
    lang = (payload.context or {}).get("lang", DEFAULT_LANG).lower()

    if lang.startswith("id"):
        reply = (
            f"Ringkasan cepat: pasar cenderung sideway. Risiko default {int(DEFAULT_RISK*100)}% per trade. "
            f"Permintaan: {msg}"
        )
    else:
        reply = (
            f"Quick take: market looks range‑bound. Default risk {int(DEFAULT_RISK*100)}% per trade. "
            f"Request: {msg}"
        )

    return PredictOut(reply=reply, meta={"source": "SatoshiDoc v1"})
