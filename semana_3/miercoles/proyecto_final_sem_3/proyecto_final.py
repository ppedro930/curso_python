import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from google import genai
from sklearn.metrics.pairwise import cosine_similarity


# mandar a traer el api key de gemini a traves del .env

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# mandar a traer los archivos


# la vacante debe ir separada ya que en base a ella se va a escoger en los demas archivos el candidato
vacante_archivo = "vacante_jd.txt"

# los curriculums si se pueden enlistar ya qye de ahi se va a escoger algun candidato
cv_archivos = ["jaun.txt", "sofita.txt", "omar.txt", "ana.txt"]



# FUNCION EMBEDDING #######  esta funcion lo que hace es vectorizar el texto para la toma de decisiones
#es decir que al vectorizar saca un puntaje y el mas alto seria el elegido para esa vacante

def obtener_embedding(texto):
    try:
        resultado = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texto
        )
        return resultado.embeddings[0].values
    except Exception as e:
        print(f"Error en embedding: {e}")
        return None



# LEER VACANTE

with open(vacante_archivo, "r", encoding="utf-8") as f:
    texto_vacante = f.read()

vector_vacante = obtener_embedding(texto_vacante)

if vector_vacante is None:
    raise Exception("No se pudo generar embedding de la vacante")



# LEER CVS Y VECTORZAR

resultados = []

for archivo in cv_archivos:
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            texto_cv = f.read()

        vector_cv = obtener_embedding(texto_cv)

        if vector_cv is None:
            continue

        # calcular similitud
        score = cosine_similarity(
            [vector_vacante],
            [vector_cv]
        )[0][0] #  aca se mide la similitud de los 2 vectores es decir [0] = un vector (ejplo devuelve [[0.87342]] )
        # y [0] lo convierte a 0.87
        #[0] = otro vector (ejplo [[0.38912]]) y ese
        # vector devuelve 0.38
        

        resultados.append({
            "archivo": archivo,
            "score_afinidad": round(score * 100, 2)  # se calcula porcentaje 
            # mostrando los que estan por encima de 70 como se muestra en la variable UMBRAL = 70
        })

    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")



# DATAFRAME ORDENADO

df = pd.DataFrame(resultados)

df = df.sort_values(by="score_afinidad", ascending=False)

print("\n===== RANKING CANDIDATOS =====\n")
print(df.to_string(index=False))


################################## punto n 3 ###################################### 


UMBRAL = 70   # porcentaje mínimo para pasar filtro

candidatos_filtrados = df[df["score_afinidad"] >= UMBRAL]

print("\n===== CANDIDATOS QUE PASAN FILTRO =====\n")
print(candidatos_filtrados.to_string(index=False))

def generar_correo(nombre_archivo, score):
    
    prompt = f"""
Eres un reclutador profesional de Recursos Humanos.

Redacta un correo breve invitando al candidato a entrevista.

DATOS:
Nombre archivo CV: {nombre_archivo}
Nivel de compatibilidad: {score}%

El correo debe ser:

- profesional
- cordial
- corto
- listo para enviar
"""

    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return respuesta.text

    except Exception as e:
        return f"Error generando correo: {e}"

print("\n--- archivo borrador generado txt listo para enviar correos de entrevistas\n")

for _, fila in candidatos_filtrados.iterrows():

    correo = generar_correo(
        fila["archivo"],
        fila["score_afinidad"]
    )

    print(f"\n--- {fila['archivo']} ---\n")
    print(correo)

    
    with open("correos_generados.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {fila['archivo']} ---\n")
        f.write(correo + "\n")

    nombre_archivo = "correos_generados.txt"
    print(f"\nArchivo llamado '{nombre_archivo}' se ha guardado correctamente")
 
#genere este archivo como un plus para mostrarlo directamente en un archivo txt, igual tambien
# los imprime aca en print(f"\n--- {fila['archivo']} ---\n")
    # print(correo)

######################## punto 4 ###################################
#por ultimo al ya tener todos los datos listos se seleccionan nada mas los que aplican y los que no, se descartan

print("\n--- generando Reporte_RRHH.csv para equipo RRHH ---\n")

reporte_final = []

for _, fila in df.iterrows():

    archivo = fila["archivo"]
    score = fila["score_afinidad"]
    
    # definir estado
    if score >= UMBRAL:
        estado = "ENTREVISTA"
        correo = generar_correo(archivo, int(score))
    else:
        estado = "RECHAZADO"
        correo = "No aplica correo (no pasa filtro)"
#crear columnas y registros en el csv
    reporte_final.append({
        "Ranking_score": score,
        "Archivo_CV": archivo,
        "Estado_Seleccion": estado,
        "Mensaje": correo
    })


# dataframe final RRHH
df_reporte = pd.DataFrame(reporte_final)

# ordenar por score
df_reporte = df_reporte.sort_values(
    by="Ranking_score",
    ascending=False
)

# guardar csv
df_reporte.to_csv(
    "Reporte_RRHH.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Reporte_RRHH.csv generado correctamente")

#la ia debe generar correo de acuerdo al puntaje