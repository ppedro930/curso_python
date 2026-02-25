from google import genai
from google.genai import types
import pandas as pd
import os
import time
from dotenv import load_dotenv
import json 

load_dotenv()  # Load environment variables from .env file

api_key = os.environ.get('GEMINI_API_KEY')  # Get API key from environment variable

if not api_key:
    print("Error: GEMINI_API_KEY no se encontro.")
    exit()
else:
    print("API key encontrada")

client = genai.Client(api_key=api_key)

LIMITE_TOTAL_FILAS = 10

TAMANO_LOTE = 5 #cuantas filas envia a la IA

data = {
    'id': range(1, 11),
    'comentario': [
        "increible servicio", "pesimo, no vuelvo", "llego tarde",
        "Me encanto el color", "Funciona bien", "Roto al llegar", "Excelente",
        "atencion de 10","no es lo que esperaba", "atencion media"
    ]
}

df = pd.DataFrame(data)

df['Analisis IA'] = None

def procesar_por_lotes(dataframe, limit, batch_size):
    peticiones_realizadas =0
    filas_procesadas = 0

    df_trabajo = dataframe.head(limit).copy()

    print(f"iniciando analisis de {len(df_trabajo)} filas en otes de...{batch_size}")

    for i in range(0, len(df_trabajo), batch_size):
        lote = df_trabajo.iloc[i:i+batch_size]

        lista_comentarios = lote[['id', 'comentario']].to_dict(orient='records')
                                  
        prompt = f"""Analiza el sentimiento de los siguientescomentarios,
        responde estrictamente en formato json con el siguiente esquema:
        {{"resultado": [{{"id":1, "sentimiento": "positivo"}}, ...]}}

        comentarios a procesar:
        {json.dumps(lista_comentarios)}
        """
        try:
            print(f"Procesando lote {i//batch_size + 1} a la IA...", end=" ")

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json"
            )
     )
            res_json = json.loads(response.text)

            for item in res_json['resultado']:
                dataframe.loc[dataframe['id'] == item['id'], 'Analisis IA'] = item['sentimiento']

            print("recibido.")
            peticiones_realizadas += 1

        except Exception as e:
            print(f"Error al procesar lote {e}")
            break #sale del ciclo
            
        time.sleep(1) #pausa entre peticiones
    
    return dataframe

df_final = procesar_por_lotes(df, LIMITE_TOTAL_FILAS, TAMANO_LOTE)

print("\n--- Resultado final---")
print(df_final.head(LIMITE_TOTAL_FILAS))

df_final.to_csv("resultados_analisis.csv", index=False)