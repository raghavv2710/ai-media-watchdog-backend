---
title: AI Media Watchdog
emoji: 🕵️‍♂️
colorFrom: red
colorTo: blue
sdk: docker
app_file: main.py
pinned: true
---

# 🛡️ AI Media Watchdog — Media Insight API

A production-ready **FastAPI** backend for real-time **sentiment** and **toxicity** analysis across **text**, **files**, and **YouTube videos**. Built for media researchers, educators, and AI enthusiasts.

-----

## 🚀 Deployment: Hugging Face Spaces (Docker)

### 🛠️ 1. Requirements

  - Python 3.10+ (see `runtime.txt`)
  - All dependencies listed in `requirements.txt`

-----

### 🐳 2. Deploy on Hugging Face (Docker SDK)

#### ✅ Step-by-Step:

1.  **Push this backend project to GitHub** (public repo).
2.  Go to [huggingface.co/spaces](https://huggingface.co/spaces) → **Create new Space**
3.  Set the following options:
      - **SDK**: `Docker`
      - **Space Name**: `ai-media-watchdog`
      - **Visibility**: `Public` (for free tier)
4.  In your repo root, ensure:
      - A valid `Dockerfile` is present
      - Entry point is `main.py` running on port **7860**
5.  In the Hugging Face Space, go to **Settings → Variables**, and add:
      - `HF_TOKEN` → Your Hugging Face token (for private model loading)
      - `ADMIN_TOKEN` → Your admin password
      - `FRONTEND_ORIGIN=https://mediawatchdog.vercel.app` (CORS allowlist)

Once deployed, your backend will be accessible at:
`https://<your-username>-ai-media-watchdog.hf.space`

Use this URL in your frontend’s `.env` as:

```env
VITE_API_URL=https://<your-username>-ai-media-watchdog.hf.space
```

-----

### 🧱 3. Project Structure

```
📦 backend/
├── main.py                  # ✅ FastAPI entrypoint
├── predict.py               # ✅ Sentiment & Toxicity classification
├── Dockerfile               # ✅ Hugging Face Docker config
├── requirements.txt         # ✅ All dependencies
├── .env                     # 🔒 (Used for local dev only)
├── extract/                 # 📄 Text & file extractors (PDF, DOCX, TXT, YouTube)
├── retraining/              # 🔁 Model retraining logic
├── storage/                 # 📦 Logs + batch data for monitoring
```

-----

### 🔍 API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| `POST`   | `/analyze_text`    | Analyze plain text                 |
| `POST`   | `/analyze_file/`   | Analyze PDF, DOCX, or TXT file     |
| `POST`   | `/analyze_youtube/`| Analyze YouTube video via URL      |
| `GET`    | `/health`          | Check server health                |
| `POST`   | `/admin/retrain`   | Trigger retraining (admin only)    |

-----

### ⚠️ Notes

  - All requests are logged to `storage/inputs_log.jsonl` (for retraining).
  - Models (`raghavv2710/sentiment-roberta-base` and `raghavv2710/toxicity-roberta-base`) are pulled from Hugging Face Hub securely using your token.
  - For long-term storage or metrics, integrate with cloud storage (e.g., S3, Supabase, GCS).

-----

### 📄 License

This project is licensed under the Apache License 2.0.

See `LICENSE` for full terms.
You are free to use, modify, distribute, and build upon this work for personal or commercial purposes — with proper attribution.

-----

### 💡 Built With

  - ⚡ **FastAPI**
  - 🤗 **Transformers**
  - 🐋 **Docker** + **Hugging Face Spaces**
  - 🧠 **Fine-tuned RoBERTa models**
  - 📑 **YouTube transcript** and **file parsing utilities**

Made with ❤️ to support safer and more transparent media.
Follow the project or contribute via GitHub\!

-----