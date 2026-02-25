from google import genai
from google.genai import types
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.environ.get('GEMINI_API_KEY')  # Get API key from environment variable

if not api_key:
    print("Error: GEMINI_API_KEY no se encontro.")
    exit()
else:
    print("API key encontrada")

client = genai.Client(api_key=api_key)

LIMITE_TOTAL_FILAS = 10

LIMITE_DIARIO = 5 #cuantas filas envia a la IA
peticiones_realizadas =0

print(f"iniciando analisis de  {LIMITE_DIARIO} peticiones ")

data = {
    'id': range(1, 6),
    'comentario': [
        "increible servicio", "pesimo, no vuelvo", "llego tarde",
        "no Me encanto el color", "llego antes de tiempo excelente"
    ]
}

df = pd.DataFrame(data)

df['Analisis_ia'] = None

def analizar_comentario(texto):

    prompt = f"""
    actua como un sicologo experto y 
    clasifica los siguientes comentarios de acuerdo al sentimiento '{texto}'
    solo responde con POSITIVO, NEGATIVO o NEUTRO, sin explicaciones ni codigo ni codigo markdown
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt, 
            config=types.GenerateContentConfig(
                temperature=0.0,
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

print("\n ---Iniciando procesamiento...---")

for index, row in df.iterrows():
    if peticiones_realizadas >= LIMITE_DIARIO:
        print(f"\n Alto:se alcanzo el limite de peticiones ({LIMITE_DIARIO}) .")
        print("guardando el proceso terminando script")
        break

    print(f"Procesando fila {index} (Peticion #{peticiones_realizadas + 1})...", end=" ")

    resultado = analizar_comentario(row['comentario'])

    peticiones_realizadas += 1

    if "429" in resultado or "quota" in resultado.lower():
        print(" Limite de peticiones alcanzado durante el procesamiento.")
        df.at[index, 'Analisis_ia'] = "Limite de peticiones alcanzado"

    df.at[index, 'Analisis_ia'] = resultado
    print(f"resultado {resultado}")
    time.sleep(4)  # Pausa para evitar sobrecargar la API

print("\n ---Proceso terminado---")
print(df.head)

df.to_csv("analisis_sentimientos.csv", index=False)


