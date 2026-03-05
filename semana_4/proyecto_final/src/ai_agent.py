import pandas as pd
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time


    # RUTAS AUTOMÁTICAS (IGUAL QUE TU PROYECTO) 
def main():

    BASE_DIR = Path(__file__).resolve().parent.parent 
    #ruta absoluta

    INPUT_FILE = BASE_DIR / "data" / "processed" / "airbnb_clustered.csv" 
    # ruta del archivo para procesar 

    OUTPUT_PATH = BASE_DIR / "data" / "processed" 
    #ruta para guardar archivos


    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    # crear carpeta si no existe


    OUTPUT_FILE = OUTPUT_PATH / "reporte_inversion_ia.md"
    # archivo a procesar y guardar





    load_dotenv()
    # busca el archivo .env
    # y busca GEMINI_API_KEY para que Python lo pueda leer como si fueran parte del sistema.

    API_KEY = os.getenv("GEMINI_API_KEY") # Busca 
    #entre las variables de entorno la que se llama 
    # 'GEMINI_API_KEY' y guarda su valor en esta variable

    if not API_KEY: #si no existe o no lo encuentra... sale el error
        raise ValueError(" No se encontró GEMINI_API_KEY en .env")

    genai.configure(api_key=API_KEY) # funcion que Valida la llave con 
    #los servidores de Google para permitir usar sus servicios de IA

    model = genai.GenerativeModel("gemini-2.5-flash-lite") 
    #funcion que le asigna el modelo 

    print("Gemini conectado") 


    # LEER DATASET


    df = pd.read_csv(INPUT_FILE) # lee el archivo que va a procesar

    print(" Dataset cargado:", df.shape) # df.shape devuelve numero de filas y columnas


    # FILTRAR MUNICIPIOS INTERESANTES


    # Cambia el nombre del cluster si el tuyo es distinto
    target_cluster = "Oportunidad" #guardar el nombre del grupo que te interesa



    df_target = df[df["cluster"] == 2].copy()

    #porque se repite df?
    #porque Filtra el DataFrame df, revisando que la columna 
    # 'cluster' de ese mismo DataFrame df sea igual a 2".
    #escogi el cluster 2 para hacer el analisis de oportunidad

    #revisa la columna "cluster" del dataframe df
    #Selecciona solo las filas donde el cluster sea igual a 2
    # el cluster 2 
    #Guarda el resultado en df_target .copy() 
    #Sin el .copy(), df_target no sería un objeto independiente, 
    #sino una "vista" o un reflejo del original

    ################################################################################################

    # Ordenar por oportunidad (ajusta columna si deseas)
    df_target = df_target.sort_values(by="price", ascending=True)

    #porque se repite df_target?
    #el Lado derecho se toma df["cluster"] == 2 
    #lo organiza por precio y se genera un "resultado ordenado".
    #Lado izquierdo toma ese "resultado ordenado". y lo guarda encima de la variable anterior.

    #sort_values se ordenan valores por precio del mas barato al mas caro

    top5 = df_target.head(5) 
    # selecciona los primeros 5 municipios segun el precio del mas barato al mas caro


    print(" Top municipios seleccionados:", len(top5))
    #len muestra solo el conteo del top 5 especificado en head(5) puedes cambiarlo pero 
    # el numero que ponga es a lo que se va hacer analisis...
    # #igual si pongo tails(5) mostraria los 5 ultmimos


    # GENERAR REPORTE IA


    reporte = "# Reporte de Inversión IA\n\n" #titulo en el archivo .md 
    #porque .md? .md es formato markdown ya que 
    # como se usa apikey Gemini suele responder 
    # con formato Markdown por defecto (negritas, listas, etc.)

    for indice, row in top5.iterrows(): #para el indice de filas (row) en top5 .iterrows() procesa
        #los datos de cada fila
        # Acceso directo porque sabes que las columnas existen
        municipio = row["neighbourhood_cleansed"]
        cluster = row["cluster"]
        precio = row["price"] 
        #en base a cada columna procesada se le dara la siguiente instruccion

    

        prompt = f"""
    Eres un consultor.

    El municipio {municipio} es tipo {cluster}.
    con costo de vida {precio}. Dame 3 pros y contras de invertir ahí.
    """
    # a traves del prompt le doy el rol de consultor 
    # ya teniendo los 5 municipios con el cluster 2 (oportunidad) y su precio
    # lo digo que me de los pros hy contras de invertir ahi

        try: #ya teniendo los datos listos para procesar con su instruccion
            #intentar hacer lo siguiente

            print(f" Analizando {municipio}...") #analizar el municipio seleccionado

            response = model.generate_content(prompt) # generar respuesta de IA segun la instruccion

            texto = response.text #como se usa IA le pedimos que devuelva solo texto string
            #ya que sin esto la IA no va a  devolver un simple "string". 
            #va a  devolver un objeto complejo que contiene metadatos 
            #(como por qué se detuvo la generación, si hubo filtros de seguridad, etc.).

            reporte += f"##  {municipio}\n\n" # asi va titulado cada municipio en el .md 
            reporte += texto + "\n\n---\n\n" # acumula el resultado de la consulta a la
            # IA segun el promt antes de guardarlo

            # evita rate limit
            time.sleep(2) #como las apis gratis tienen un límite de RPM (peticiones por minuto).
            # evita el error 429

        except Exception as e: # si no logra consultar algun municipio lanza error

            print(f"⚠️ Error con {municipio}: {e}")

            reporte += f"## {municipio}\nError al consultar IA\n\n"


    # GUARDAR REPORTE


    with open(OUTPUT_FILE, "w", encoding="utf-8") as f: 
        # con la funcion open se le da la variable del archivo para escribir con
        # texto codificado a  formato utf-8 con el alias f=archivo
        f.write(reporte) #se usa el alias de la variable ya con el archivo para escribirlo 
        #con los resultados

    print("\n✅ REPORTE GENERADO")
    print("📄", OUTPUT_FILE) #solo indica que el archivo si se pudo 
    #generar con su ubicacion y su nombre

if __name__ == "__main__":
    main()