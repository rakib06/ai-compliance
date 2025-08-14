import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
ENV_PATH = find_dotenv(usecwd=True)

if not ENV_PATH:
    # repo root is two levels up from this file: backend/<this file>
    ENV_PATH = str(Path(__file__).resolve().parents[1] / ".env")

loaded = load_dotenv(ENV_PATH)
                     
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")  # or 'textract'
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "data/faiss.index")))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
