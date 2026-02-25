import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print(f"id del modelo | Tipo de acciones")
print("-"*80)

try:
    for model in client.models.list():
        action = model.supported_actions or []
        
        if 'generateContent' in action:
            display_name = model.display_name or "sin nombre"
            print(f"{model.name} | {action}")

except Exception as e:
    print(f"Error es: {e}")










