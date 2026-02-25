import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

imagen_path = "etiqueta_nutria.jpg"

try:
    imagen = Image.open(imagen_path)
    print(f"--- imagen{imagen_path} cargada")
    print("analizando")
except FileNotFoundError:
    print(f"error : no se encontro {imagen_path}")
    exit()

prompt= """
Analiza esta imagen de info nutricional.
tu objetivo es extraer los macronutrientes principales y el tamaño de la porcion.

devuelve un objeto JSON estricto con las siguientes claves y tipos de datso.
intenta normalizar los valores numericos (quita las 'g' o 'mg').

- product_name (string, inventa un nombre generico basado en lo que veas, ej: "cereal generico")
- serving_size (string ej: "1 cup (50g)")
- calories (int)
- total_fag_g (float, usa 0.0 si no se encuentra)
- protein_g (float, usa 0.0 si no se encuentra)
- sodium_g (int, usa 0 si no se encuentra)

si algun dato no es visible, usa null o 0 para numeros.
"""
try:
    response =client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[prompt,imagen],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    
    data_dict = json.loads(response.text)
    print("\n nutrientes extraidos exitosamente\n")

    print(f"producto detectado: {data_dict.get('product_name')}")
    print(f"Calorias por porcion {data_dict.get('calories')}")

    #print(f"json completo \n{response.text}")

    df_nutricion = pd.DataFrame([data_dict])

    df_nutricion['fecha_registro'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n df generado")
    print(df_nutricion)

    csv_filename = "diario_nutricional.csv"

    header_mode = not os.path.exists(csv_filename)

    df_nutricion.to_csv(csv_filename, mode='a', index=False, header=header_mode)

except json.JSONDecodeError:
    print("error eso no fue un json valido")
    print("respuesta cruda", response.text)
except Exception as e:
    print(f"ocurrio un error {e}")
    



