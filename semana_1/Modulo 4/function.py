import pandas as pd
from pathlib import Path

def concat_archivos_csv(carpeta_input,nombre_archivo_salida):
    
    path_input=Path(carpeta_input)
    path_salida = Path(nombre_archivo_salida)

    patron = "Sales_*.csv"
    archivos = list(path_input.glob(patron))

    if not archivos:
        print(f"No se encontraron ningun archivo en la carpeta {path_input.absolute()}")
        print(f"ningun archivo coincide con el patron {patron}")
        print(f"iniciando proceso de {len(archivos)} archivos...")
        return None

    lista_temporal =[]
    for file in archivos:
        df_mes = pd.read_csv(file)
        lista_temporal.append(df_mes)
        print(f"leyendo{file.name}")

    df_unido = pd.concat(lista_temporal, ignore_index=True)

    path_salida.parent.mkdir(parents=True, exist_ok=True)

    df_unido.to_csv(path_salida, index=False)

    return df_unido

ruta_entrada = "./Sales_Data"
name_file_output = "Reporte_Ventas_2019.csv"
mi_csv_unido = concat_archivos_csv("./Sales_Data", "ventas_cafe_unido.csv")





