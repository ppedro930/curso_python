import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print("--- lista de modelos (sin filtros) ---")
try:
    for model in client.models.list():
        print(f"ID modelo: {model.name}")
        print(f"Nombre: {model.display_name}")
        print("**"*25)

except Exception as e:
    print(f"Error  criticos: {e}")






