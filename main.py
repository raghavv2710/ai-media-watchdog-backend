"""
✅ FastAPI entry point for AI Media Watchdog
Routes: /analyze_text, /analyze_file, /analyze_youtube, /admin/retrain, /health
"""

from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil, os, uuid, json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from predict import classify
from extract.doc_parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from extract.youtube_transcript import get_youtube_transcript
from extract.utils import clean_text
from retraining.monitor import monitor_and_trigger

app = FastAPI(title="Media Insight API")

# ✅ Secure CORS: allow only your frontend to access the API
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://mediawatchdog.vercel.app")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Request model
class TextInput(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/analyze_text")
def analyze_text(data: TextInput):
    cleaned = clean_text(data.text)
    result = classify(cleaned)
    log_input(data.text, result)
    return {"result": result}

@app.post("/analyze_file/")
async def analyze_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    temp_path = f"temp/{uuid.uuid4()}.{file_ext}"
    os.makedirs("temp", exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file_ext == "pdf":
        raw_text = extract_text_from_pdf(temp_path)
    elif file_ext == "docx":
        raw_text = extract_text_from_docx(temp_path)
    elif file_ext == "txt":
        raw_text = extract_text_from_txt(temp_path)
    else:
        os.remove(temp_path)
        return {"error": "Unsupported file type"}

    os.remove(temp_path)
    cleaned = clean_text(raw_text)
    result = classify(cleaned)
    log_input(raw_text, result)
    return {"result": result}

@app.post("/analyze_youtube/")
def analyze_youtube(url: str = Form(...)):
    raw_text = get_youtube_transcript(url)
    cleaned = clean_text(raw_text)
    result = classify(cleaned)
    log_input(raw_text, result)
    return {"result": result}

# ✅ Save input and result for retraining
def log_input(text: str, result: dict):
    log_path = "storage/inputs_log.jsonl"
    os.makedirs("storage", exist_ok=True)
    log_entry = {
        "id": str(uuid.uuid4()),
        "text": text[:1000],
        "sentiment": result["sentiment"],
        "toxicity": result["toxicity"]
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

# ✅ Admin auth via header token
def admin_auth(x_admin_token: Optional[str] = Header(None)):
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme")
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return True

@app.post("/admin/retrain")
def admin_retrain(admin: bool = Depends(admin_auth)):
    result = monitor_and_trigger()
    return {"message": result}
