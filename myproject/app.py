from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from databse import create_table, get_prediction_history, save_prediction

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "spam_model.pkl"
FRONTEND_PATH = BASE_DIR / "template" / "page.html"

app = FastAPI(title="Spam Detection API")
model = joblib.load(MODEL_PATH)
create_table()


class MessageInput(BaseModel):
    message: str


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_PATH)


@app.post("/predict")
def predict(data: MessageInput) -> dict[str, str]:
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Please enter a message.")

    prediction = model.predict([message])[0]
    prediction_label = str(prediction).strip().lower()

    if prediction_label in ("1", "spam"):
        result = "spam"
    elif prediction_label in ("0", "ham", "not spam"):
        result = "ham"
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected model prediction: {prediction}",
        )

    save_prediction(message, result)
    return {"prediction": result}


@app.get("/history")
def prediction_history() -> list[dict]:
    return get_prediction_history()
