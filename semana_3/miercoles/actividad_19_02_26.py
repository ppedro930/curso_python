import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# LEER texto como resolver un proble de prog apuntes.de ...... 

# leer archivo solo una vez, si quieres leer varios es por lista

with open("politicas.txt", "r", encoding="utf-8") as f:
    texto = f.read()


#############objetivo principal...  - separarlo por temas
import re
#### entonces se crea la funcion de separar temas anexando la variable texto (archivo.txt) el cual 
#### lo lee para identificar y ejecutar la funcion
#\n = salto de línea, \d+ detecta uno o más números y \. muestra todos los titulos y subtitulos
def separar_temas(texto):

    partes = re.split(r"\n\d+\.", texto) #re. split se especifica lo que se va a dividir

    temas = {}

    for p in partes:
        p = p.strip()
        if not p:
            continue
        
        lineas = p.split("\n", 1)
        titulo = lineas[0].strip()
        contenido = lineas[1].strip() if len(lineas) > 1 else ""
        
        temas[titulo] = contenido

    return temas


temas = separar_temas(texto)

for t in temas:
    print(t)

################## aca finaliza la separacion por temas y no es necesario la IA



###########################################################################################

def obtener_embedding(texto):
    try:
        resultado = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texto
        )
        
        #prints para debug

        #print(f"error en embeddings\n{resultado.embeddings},\n")
        #print(f"primer resultado de embeddings \n{resultado.embeddings[0]}")
        #print(f"\n primer resultado {resultado.embeddings[0].values}")

        return resultado.embeddings[0].values
    except Exception as e:
        print(f"error en embedding: {e}")
        return[]

#obtener_embedding(texto)
#lo anterior es la funcion que vectoriza el texto 



###########################################

###########################################



#  Paso 2: El Buscador de "Sentido Común"
# para ejecutar la indexacion se crea una funcion anexando la variable temas 

def indexar_temas(temas):
    indice = {}

    print("\nIndexando reglas:")
    for titulo, contenido in temas.items():

        # puedes usar título + contenido para mejor contexto
        texto_completo = f"{titulo}\n{contenido}"

        vector = obtener_embedding(texto_completo)

        if len(vector) > 0:
            indice[titulo] = vector
            print(".", end="", flush=True)   # <- muestra puntos en pantalla

    print("\nIndexación terminada\n")
    print(f"")
    return indice


# EJECUTAR INDEXACIÓN
indice_vectores = indexar_temas(temas)

#############################
#aca finaliza el paso 2 
  

###########################################
##ahora, paso 3  Configurar el "Filtro de Verdad"

def pregunta_verif_funcionamiento(pregunta, temas, indice_vectores):

    # 1) vectorizar pregunta
    vector_pregunta = obtener_embedding(pregunta)

    if len(vector_pregunta) == 0:
        return "Error generando embedding"

    # 2) buscar tema más parecido
    mejor_tema = None
    mejor_score = -1

    for titulo, vector in indice_vectores.items():

        score = cosine_similarity(
            [vector_pregunta],
            [vector]
        )[0][0]

        if score > mejor_score:
            mejor_score = score
            mejor_tema = titulo

    # 3) si la similitud es muy baja → no está en reglamento
    if mejor_score < 0.45:
        return "Lo siento, esa información no está en mis políticas vigentes"


    # 4) obtener texto del reglamento encontrado
    contexto = f"{mejor_tema}\n{temas[mejor_tema]}"


 ##############################################################################3 

#prompt normal... por default
    
    #Eres un experto en Recursos Humanos.

#Responde SOLO usando la información del reglamento proporcionado.

#Si la respuesta NO está en el reglamento, di EXACTAMENTE:
#Lo siento, esa información no está en mis políticas vigentes

##########################################################################

#prompt de mayordomo
###############################
#Eres un MAYORDOMO extremadamente educado, profesional y refinado.

#Hablas con cortesía absoluta, lenguaje formal y tono respetuoso.
#NO inventas información.
#Respondes SOLO usando la información del reglamento proporcionado.

#Si la respuesta NO está en el reglamento, di EXACTAMENTE:
#Lo siento, esa información no está en mis políticas vigentes

################################################

################prompt de cambio de personalidad a sargento


#Eres un SARGENTO MILITAR extremadamente estricto y disciplinado.

#Hablas con órdenes claras, tono firme y directo, como en el ejército.
#NO inventas información.
#Respondes SOLO usando la información del reglamento proporcionado.

#Si la respuesta NO está en el reglamento, di EXACTAMENTE:
#Lo siento, esa información no está en mis políticas vigentes

#RESPUESTA (tono militar estricto):


################prompt de cambio de personalidad a sargento


    # 5) PROMPT RH CON FILTRO DE VERDAD
    prompt = f"""
Eres un SARGENTO MILITAR extremadamente estricto y disciplinado.

Hablas con órdenes claras, tono firme y directo, como en el ejército.
NO inventas información.
Respondes SOLO usando la información del reglamento proporcionado.

Si la respuesta NO está en el reglamento, di EXACTAMENTE:
Lo siento, esa información no está en mis políticas vigentes

REGLAMENTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA (tono militar estricto):
"""


    # 6) llamar a Gemini
    respuesta = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

# forma segura de obtener texto
    try:
        return respuesta.text
    except:
        
        return respuesta.candidates[0].content.parts[0].text



#print(pregunta_verif_funcionamiento(
#    "¿Puedo usar el Wi-Fi del Starbucks para revisar la banca de la empresa?",
#    temas,
#    indice_vectores
#))

pregunta = input("pregunta algun tema relacionado con nuestras politicas: ")

respuesta = pregunta_verif_funcionamiento(
    pregunta,
    temas,
    indice_vectores
)

print(respuesta)


