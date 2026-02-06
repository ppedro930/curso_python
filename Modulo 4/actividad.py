import os
import glob
import pandas as pd


def concat_archivos_csv(carpeta_input, nombre_archivo_salida):

    patron = "Sales_*.csv"
    ruta_patron = os.path.join(carpeta_input, patron)

    archivos = glob.glob(ruta_patron)

    if not archivos:
        print(f"No se encontraron archivos en la carpeta {os.path.abspath(carpeta_input)}")
        print(f"Ningún archivo coincide con el patrón {patron}")
        return None

    print(f"Iniciando proceso de {len(archivos)} archivos...\n")

    lista_temporal = []

    for file in archivos:
        print(f"Leyendo {os.path.basename(file)}")
        df = pd.read_csv(file)
        lista_temporal.append(df)

    # Concatenar todos los DataFrames
    df_final = pd.concat(lista_temporal, ignore_index=True)

    # Crear carpeta de salida si no existe
    carpeta_salida = os.path.dirname(nombre_archivo_salida)
    if carpeta_salida:
        os.makedirs(carpeta_salida, exist_ok=True)

    # Guardar archivo final
    df_final.to_csv(nombre_archivo_salida, index=False)

    print(f"\nArchivo creado correctamente: {nombre_archivo_salida}")

    return df_final


# -------------------------------
# EJECUCIÓN
# -------------------------------
ruta_entrada = "./Sales_Data"
name_file_output = "ventas_cafe_unido.csv"

mi_csv_unido = concat_archivos_csv(ruta_entrada, name_file_output)
