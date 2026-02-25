import argparse
import pandas as pd
import os
import sys
from pathlib import Path


raiz_folder = Path(__file__).parent.parent

ruta_motor_ia = (raiz_folder / 'martes').resolve()

sys.path.append(str(ruta_motor_ia))

from motor_ia import analizar_sentimiento

def ejecutar_automatizacion():

    parser = argparse.ArgumentParser(description="analizador de sentimientos")

    parser.add_argument("--archivo", type=str, required=True, help="nombre del archivo csv de entrada")
    parser.add_argument("--columna", type=str, required=True, help="nombre de la columna a analizar")
    parser.add_argument("--salida", type=str, default="resultado_sentimientos.csv", help="nombre del archivo de salida")

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
    
    if args.columna not in df.columns:
        print(f"Error: La columna '{args.columna}' no se encuentra en el csv.")
        return
    sentimientos = []
    tiempos = []
    modelos = []

    print(f"procesando {len(df)} filas con IA. por favor espere... \n")

    for index, fila in df.iterrows():
        texto = str(fila[args.columna])
        resultado, tiempo, t_in, t_out, model_id = analizar_sentimiento(texto)

        sentimientos.append(resultado)
        tiempos.append(tiempo)
        modelos.append(model_id)

        print(f"fila {index+1}:{resultado} ({tiempo}s)")

    df['Sentimiento IA'] = sentimientos
    df['Tiempo ejecucion'] = tiempos
    df['Modelo usado'] = modelos

    df.to_csv(args.salida, index=False)

    print(f"\nProceso terminado. '")
    print(f"Resultados guardados en '{args.salida}'")

if __name__ == "__main__":
    ejecutar_automatizacion()

# python main.py --archivo analisis_sentimiento_ia_json.csv --columna comentario --salida resultados_sentimientos2.csv

#producto slogan imagenpromt pegarloa otro chat y agregarla
