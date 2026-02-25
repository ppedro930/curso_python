import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("error: no se encontro el api key.")

try:
    client = genai.Client(api_key=API_KEY)
    print("cliente conectado y listo.")
except Exception as e:
    print(f"error al conectar el cliente: {e}")
    exit()



# FUNCION ANALIZAR IMAGEN

def analizar_imagen(img_bytes):

    prompt = """
Dime los nombres de los personajes que aparecen en esta imagen.
Responde solo con los nombres separados por coma.
"""

    configuracion = types.GenerateContentConfig(
        temperature=0.0,
        top_k=20,
        top_p=0.95,
        candidate_count=1
    )

    print(f"\nAnalizando imagen... {img_bytes}")
    inicio = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Part.from_text(text=prompt),types.Part.from_bytes(
                    data=img_bytes,
                    mime_type="image/png")
            ],
            config=configuracion
        )

        t_in = getattr(response.usage_metadata, "prompt_token_count", 0) if response.usage_metadata else 0
        t_out = getattr(response.usage_metadata, "candidates_token_count", 0) if response.usage_metadata else 0

        fin = time.time()
        duracion = round(fin - inicio, 2)

        return response.text.strip(), duracion, t_in, t_out

    except Exception as e:
        return f"Error API: {str(e)}", 0, 0, 0



# LEER IMAGEN

with open("bob_esponja_promt.png", "rb") as f:
    imagen_bytes = f.read()



# LLAMAR FUNCION

texto, tiempo, tokens_in, tokens_out = analizar_imagen(imagen_bytes)

print("\nRespuesta del modelo:")
print(texto)
print(f"\nTiempo de respuesta: {tiempo} segundos")
print(f"Tokens utilizados: {tokens_in} entrada + {tokens_out} salida = {tokens_in + tokens_out}")
print("**"*25)
