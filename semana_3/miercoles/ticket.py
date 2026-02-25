import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

imagen_path = "ticket.png"

try:
    imagen = Image.open(imagen_path)
    print(f"--- imagen{imagen_path} cargada")
    print("analizando")
except FileNotFoundError:
    print(f"error : no se encontro {imagen_path}")
    exit()

imagen =Image.open(imagen_path)

print("---analizando imagen con vision AI...---")


prompt= """
Analiza esta imagen de un ticket de compra.
Extrae la siguiente informacion en formato JSON estricto:
- tienda (string)
- fecha (string formato YYYY-MM-DD)
- total (float)
- items (lista de objetos con 'producto' y 'precio')

si algun dato no es visible, usa null.
"""

response = client.models.generate_content(
    model ="gemini-2.5-flash-lite",
    contents=[prompt, imagen],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.1
    )
)

#print(response.text)

try:
    data_dict = json.loads(response.text)
    print("\n!datos extraidos con exito!")
    print(f"tienda: {data_dict['tienda']}")
    print(f"total: ${data_dict['total']}")

    df_items = pd.DataFrame(data_dict['items'])

    

    df_items['tienda'] = data_dict['tienda']
    df_items['fecha'] = data_dict['fecha']
    df_items['total'] = data_dict['total']

    print("\n--- dataframe generado")

    print(df_items)

    df_items.to_csv("ticket_digitalizado.csv", index=False)

    

    print(f"bolsa: {data_dict['items'][3]['producto']}")

except Exception as e:
    print(f"error parseando json {e}")
    print("respuesta cruda:", response.text)
#imprimir total y cualquier otro item (bolsa) y otro df donde guarde tienda y fecha