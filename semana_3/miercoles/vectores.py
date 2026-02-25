import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

peliculas = [
    {"titulo": "Titanic",
     "trama": "Un barco gigante choca con un iceberg y se hunde en el atlantico."},
    {"titulo": "el rey leon",
     "trama": "un  cachorro de leon huye de su reino tras la muerte de su padre y aprende a madurar "},
    {"titulo": "interestelar",
     "trama": "Un grupo de astronautas viaja a través de un agujero de gusano en busca de un nuevo hogar para la humanidad."},
    {"titulo": "buscando a nemo",
     "trama": "un pez padre cruza el oceano para encontrar a su hijo perdido."}
]

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

#obtener_embedding(peliculas[0]['trama'])

'''
la funcion obtener_embedding permite convertir en vectores las palabras que le pasemos, con el fin de encontrar 
si las palabras son similares, opuestas o no tienen relacion entre si las palabrasson similares
opuestas o no tienen relacion entre si
esto se puede hacer gracias al modelo gemini-embedding-001 

'''

print("---1 vectorizando base de datos (esto tarda un poco)...---")

matriz_embedding =[]

for peli in peliculas:
    vector = obtener_embedding(peli['trama'])
    matriz_embedding.append(vector)

matriz_embedding= np.array(matriz_embedding)

usuario_query = input("\n¿Que tienes ganas de ver hoy? (ej el 'algo de viajes especiales' o 'animales tristes')")
vector_usuario = np.array([obtener_embedding(usuario_query)])

'''
vector usuario es el vector (numeros) de la pelicula o tema que quiere ver el usuario
'''

similitud = cosine_similarity(vector_usuario, matriz_embedding)

'''
la herramienta cosine_similarity (similitud de coseno) permite transformar cada palabra de un texto a
un vector (una flecha con direccion, magnitud y sentido en un espacio tridimensional)
esta herramienta solo toma en cuenta el sentido sin importarle la direccion o magnitus.

el sentido es la direccion hacia donde apuntas las flechas representadas por el vector

como funciona?

| Situación    | Ángulo de las flechas | Coseno (Similitud) | Significado                                     |
| ------------ | --------------------- | ------------------ | ----------------------------------------------- |
| Idénticos    | Apuntan igual (0°)    | 1.0 (Máximo)       | "Perro" vs "Perro"                              |
| Relacionados | Ángulo cerrado        | 0.8 - 0.9          | "Barco" vs "Océano"                             |
| Nada que ver | Ángulo de 90°         | 0.0                | "Titanic" vs "Hamburguesa"                      |
| Opuestos     | Ángulo de 180°        | -1.0               | (Raro en texto, más común en matemáticas puras) |

¿como funciona este ejemplo?

    1.- calcula el vector (la flecha) de lo que el usuario desea (usuario query)
    2.- toma ese vector (vector usuario) y lo compara con las peliculas.
    3.- toma los 4 vectores de las peliculas gracias a la matriz (matriz_embedding)
    4.- Calcula el angilo entre la flecha del usuario y las 4 flechs de las peliculas al mismo tiempo.
    5.- devuelve una lista de puntuaciones entre el 0 y el 1.

'''

#print(similitud)

indice_ganador = np.argmax(similitud)
match = peliculas[indice_ganador]
#print(indice_ganador)
score = similitud[0][indice_ganador]

print(f"\n te recomiendo: '{match['titulo']}'!'")
print(f"porcentaje de coincidencia:{score:.4f}")
print(f"trama: {match['trama']}")

print("\n--- 4. generando explicacion personalizada (el toque humano)")

prompt_rag = f"""

actua como un recomendador de cine experto y carismatico.

INFORMACION DEL SISTEMA:
- el usuario busco "{usuario_query}"
- nuestra base de datos encontrom la mejor coincidencia: "{match['titulo']}"
- la trama es: "{match['trama']}"

tu tarea:
explicale al usuario brevemente porque esta pelicula es perfecta para su busqueda.
se convincente y amable. no menciones "vectores" ni "embeddings", solo habla de la pelicula.

"""

modelos_a_probar = ["gemini-2.5-flash-lite", "gemini--flash-lite-latest", "gemini-flash-latest", "gemini-2.5-flash",
                    "gemini-3-flash-preview"]
explicacion_generada = False

for modelo_name in modelos_a_probar:
    try:
        response = client.models.generate_content(
            model=modelo_name,
            contents=prompt_rag,
            config=types.GenerateContentConfig(
                temperature=0.0
            )
        )

        print(f"asistente ({modelo_name}): \n{response.text}")
        explicacion_generada =True
        break

    except Exception as e:
        print(f"el modelo {modelo_name} no esta disponible. (error:503/429). intentando con el siguiente...")

if not explicacion_generada:
    print(f"todos los modelos estan saturados, pero la mejor opcion es '{match['titulo']}'")





