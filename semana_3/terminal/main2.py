import argparse
import pandas as pd
import os
import sys
from pathlib import Path
from google.genai import types



raiz_folder = Path(__file__).parent.parent
ruta_motor_ia = (raiz_folder / 'martes').resolve()
sys.path.append(str(ruta_motor_ia))

#se debe llevar ese orden ya que arriba trae el archico con esas variables y parametros
from motor_ia2 import analizar_sentimiento, client # aca se manda a traer la funcion... no se debe hacer al principio
#da este error No module named 'motor_ia2' 
#todo debe llevar un orden en python porque ocurren errores

def buscar_columna_real(df, nombre):
    for c in df.columns:
        if c.lower().strip() == nombre.lower().strip():
            return c
    return None


####################################################################





def generar_respuesta(texto_usuario, sentimiento, contexto="", temperatura=0.7):

    instruccion_sistema = (
        "Eres un asistente experto en atención al cliente. "
        "Según el sentimiento del comentario, genera una respuesta profesional y natural. "
        "No uses markdown. Solo escribe la respuesta."
    )

    prompt = f"""
Comentario del cliente:
{texto_usuario}

Sentimiento detectado:
{sentimiento}

Genera una respuesta adecuada.
"""

    configuracion = types.GenerateContentConfig(
        system_instruction=instruccion_sistema,
        temperature=temperatura,
        top_p=0.95,
        top_k=20,
        candidate_count=1
    )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[prompt],
            config=configuracion
        )

        return response.text.strip()

    except Exception as e:
        return f"Error generando respuesta: {str(e)}"







####################################################################


def ejecutar_automatizacion():

    parser = argparse.ArgumentParser(description="Analizador de sentimientos con IA")
    parser.add_argument("--archivo", type=str, required=True)
    parser.add_argument("--columna", type=str, required=True)
    parser.add_argument("--columna2", type=str, required=False)
    parser.add_argument("--salida", type=str, default="resultado_sentimientos.csv")

    args = parser.parse_args()

    if not os.path.exists(args.archivo):
        print(f"Error: El archivo '{args.archivo}' no existe.")
        return

    print(f"cargando archivo {args.archivo}...")

    try:
        df = pd.read_csv(args.archivo, on_bad_lines='warn', engine='python')
    except Exception as e:
        print(f"Error critico al leer el archivo: {e}")
        return

    print("\nColumnas detectadas:")
    print(list(df.columns))

    columna_real = buscar_columna_real(df, args.columna)

    if columna_real is None:
        print(f"\nLa columna '{args.columna}' NO existe.")
        return

    columna2_real = None
    if args.columna2:
        columna2_real = buscar_columna_real(df, args.columna2)
        if columna2_real is None:
            print(f"\nLa columna extra '{args.columna2}' no existe. Se ignorará.")

    print(f"\nProcesando {len(df)} filas con IA...\n")

    #sugerencias = [] se creaaaa
    sentimientos = []
    tiempos = []
    modelos = []
    respuestas = []

    for index, fila in df.iterrows():

        if columna2_real:
            texto = str(fila[columna2_real])
        else:
            texto = str(fila[columna_real])

        sentimiento, tiempo, t_in, t_out, model_id = analizar_sentimiento(texto)

        respuesta = generar_respuesta(texto, sentimiento, "", 0.7)
        sentimientos.append(sentimiento)
        # sugerencias.append("") se crea vaciooo
        tiempos.append(tiempo)
        modelos.append(model_id)
        respuestas.append(respuesta)


        
        print(f"fila {index+1}: {tiempo}s")


    df['Sentimiento IA'] = sentimientos
    #df['Sugerencia'] = sugerencias ## se creaaaaa
    df['Tiempo ejecucion'] = tiempos
    df['Modelo usado'] = modelos
    df['Respuesta_Sugerida'] = respuestas


    df.to_csv(args.salida, index=False)

    print("\nProceso terminado.")
    print(f"Resultados guardados en '{args.salida}'")


if __name__ == "__main__":
    ejecutar_automatizacion()

    

# python main2.py --archivo analisis_sentimiento_ia_json.csv --columna comentario --columna2 sugerencia --salida resultados_sentimientos2.csv

#producto slogan imagenpromt pegarloa otro chat y agregarla

