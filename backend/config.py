import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")  # or 'textract'
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "data/faiss.index")))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
