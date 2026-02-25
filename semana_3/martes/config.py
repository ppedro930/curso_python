import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

base_path = Path(__file__).resolve().parent.parent

env_path = base_path / ".env"

load_dotenv(dotenv_path=env_path)

#print(f"path base {base_path}")
#print(f"path env {env_path}")

API_KEY_NAME = "GEMINI_API_KEY"

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(f"Buscando .env en: {base_path}")
    raise ValueError(f"error: no se encontro la API KEY {API_KEY_NAME}")

try:
    client = genai.Client(api_key=API_KEY)
    print("cliente conectado, wiiiiiiii")
except Exception as e:
    raise RuntimeError(f"error: {e}")  



