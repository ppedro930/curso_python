import pandas as pd

from pathlib import Path


donde_estoy = Path.cwd() # me dice donde estoy ubicado la ruta actual donde se ejecuta el codigo

ruta_carpeta = Path("./Sales_Data")  # el./sales data es la carpeta donde se encuentran los archivos csv

archivos_csv = list(ruta_carpeta.glob("Sales_*.csv")) # glob es una funcion de pathlib que me permite buscar archivos con un patron especifico, en este caso todos los archivos con extension .csv en la carpeta Sales_Data

print(f"Cantidad de archivos encontrados: {len(archivos_csv)} los cuales son para procesar")

lista_df = []

for archivo in archivos_csv:
    df_mes = pd.read_csv(archivo) # pd.read_csv es una funcion de pandas que me permite leer un archivo csv y convertirlo en un dataframe
    lista_df.append(df_mes) # append es una funcion de las listas que me permite agregar un elemento al final de la lista

    print(F"Archivo {archivo.name} cargado correctamente") # f es para formatear la cadena de texto y mostrar el nombre del archivo que se cargo

df_anual = pd.concat(lista_df, ignore_index=True) # pd.concat es una funcion de pandas que me permite concatenar varios dataframes en uno solo, ignore_index=True es para resetear el indice del nuevo dataframe

print("----------datos unidos---------")
print(df_anual.info())



