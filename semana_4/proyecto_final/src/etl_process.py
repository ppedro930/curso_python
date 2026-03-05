import pandas as pd
from pathlib import Path
import glob


def main():

    BASE_DIR = Path(__file__).resolve().parent.parent 
    # Se obtiene la ruta absoluta del directorio donde se encuentra este script.
    # __file__ representa la ruta del archivo actual y resolve().parent permite
    # obtener la carpeta raíz del proyecto para construir rutas relativas.
    RAW_PATH = BASE_DIR / "data" / "raw" 
    #aca se le indica esta ruta diciendole donde estan los archivos a procesar
    PROCESSED_PATH = BASE_DIR / "data" / "processed"
    #aca se le indica esta ruta diciendole donde se van a guardar los archivos procesados

    PROCESSED_PATH.mkdir(parents=True, exist_ok=True) 
    #todo esto indica que si las carpetas / "data" / "processed" no existen 
    #en la ruta indicada se crean automaticamente 
    #si ya existen no hace nada... por eso se especifica en la opcion booleana con parents y exist_ok


    # FUNCIONES DE LIMPIEZA


    def clean_price(x): #se crea la funcion de limpieza del campo price del df el 
        #alias de x es una variable para que se guarde ahi para que despues se aplique
        if pd.isna(x): # condicional (si hay valores vacios)
            return None # regresa valores nulos o vacios
        try:
            return float(str(x).replace("$", "").replace(",", "").strip()) #ahora esto agarra el formato 
        #string de los datos que encuentra y los convierte a float y con replace borra 
        # el signo pesos y las comas y strip elimina espacios en blanco
        # todo esto es para que no haiga conflicto alguno al momento de hacer la conversion 
        #en la columna price.., la cual se especifica mas abajo al aplicar los cambios

        except:
            return None # y la excepcion es para que regrese valores nulos o vacios


    def clean_text(series): #se define otra funcion de neighbourhood_cleansed y producto
        return series.astype(str).str.upper().str.strip() # .astype(str)procesa todo el texto (string).
    # .str.upper() pasa todo a mayuscula 
    # .str.strip() Elimina los espacios en blanco al principio y al final



    # AIRBNB archivos que se vana procesar


    def process_airbnb(file): 
    #se define la funcion para la limpieza del archivo

        print("\n========== PROCESANDO AIRBNB ==========")
        print("Archivo:", file) 
        # muestra el archivo que se va a procesar para pasar los datos al otro archivo (airbnb_clean.csv)

        df = pd.read_csv(file) # lee el archivo (airbnb.csv)

        filas_antes = len(df) #muestra las filas por default de (airbnb.csv)

        if "price" in df.columns: #si encuentra precio en el dataframe hacer lo siguiente
            df["price"] = df["price"].apply(clean_price)
    
            # df["price"] = df["price"] asigna el resultado a esa misma columna por eso se pone 2 veces
            # clean_price  es la funcion que hizo y guardo el proceso de conversion a float
            # .apply es la funcion encargada de aplicar esos cambios
            
        if "neighbourhood_cleansed" in df.columns: # si encuentra neighbourhood_cleansed haz lo siguiente
            df["neighbourhood_cleansed"] = clean_text(df["neighbourhood_cleansed"]) 
            #corrige pasando a mayusculas pasa a string y borra espacios como se le indico con clean_text
            #para despues guardarlos en esa columna pero en el nuevo archivo (airbnb_clean.csv)

        if "price" in df.columns: 
        # la condicional revisa si existe una columna llamada "price" 
        # para evitar errores si el archivo no la tiene
            df = df[df["price"] < 20000]

    #df = df[...] se pone para seleccionar las respuestas (mascara booleana)
    # de la pregunta que le esta haciendo 
    # df["price"] < 20000 = cuales son los valores que no pasan de 20000?
    # entonces como ya esta convertido a valor numerico df = df[...] va a reconocer 
    # los valores por debajo de 20000 y en automatico los guarda 
    # y borra las demas columnas para que no se vea vacio lo que esta por encima de 20000
    #es decir 
    # borra las demas columnas neighbourhood_cleansed... y demas que tengan price por encima de 20000

        filas_despues = len(df) #dice cuántos datos quedaron tras la limpieza

        print("Filas antes:", filas_antes)
        print("Filas después:", filas_despues)
        # esto lo dice todo tal cual (muestra resultados)

        print("\n--- INFO GENERAL AIRBNB ---")
        df.info() # muestra el total de columnas y filas antes de procesar y despues de procesar 


        #print("\n--- MUESTRA AIRBNB LIMPIO ---")
        #print(df.head(5).to_string()) # lo comente porque no es necesario 
        # mostrarlo en consola muestra datos generales procesados

        if "price" in df.columns:
            print("\n--- INFO PRECIOS ---")
            print(df["price"].describe()) # muestra los precios convertidos a float

        output = PROCESSED_PATH / "airbnb_clean.csv" #esto asigna el nombre del archivo (limpio) y lo guarda en output
        df.to_csv(output, index=False, encoding="utf-8-sig") #aca tambien se le da el formato de 
        #texto para que identifique las tildes 
    
        print(" Guardado:", output) #esto me indica que airbnb se guardo correctamente y muestra la ruta donde se guardo



    # ###################################                        DATOS PROFECO                       ####################################


    def process_profeco(files): # se define la funcion para buscar los archivos a procesar

        print("\n========== PROCESANDO PROFECO ==========")
        print("Archivos encontrados:", len(files)) # aca se hace la busqueda para saber la cantidad de archivos que existen

        dfs = [] #se crea una lista vacía la cual servirá como "contenedor" para guardar varios DataFrames

        for f in files: # inicio de un bucle o ciclo que sirve para recorrer, uno por uno, los archivos que hay en la lista
            print("Leyendo:", f) #muestra el progreso de los archivos que va encontrando
            try: # Intenta leer el archivo f y guardarlo con append en la lista dfs
                dfs.append(pd.read_csv(f))
            except Exception as e:
                print("Error leyendo:", f, e) # Captura cualquier tipo de error que ocurra en la busqueda de archivos. 
                #y Guarda el nombre del error (el motivo del fallo) en la variable e
    
        if not dfs:
            print(" No se pudo leer ningún archivo Profeco")
            return
        # esta condicional Sirve para detener el proceso si algo salió mal y no se cargó ningún archivo o dato.

        df = pd.concat(dfs, ignore_index=True) # toma la lista (archivos encontrados) para crear un  solo dataframe

        filas_antes = len(df) #se cuentan todas filas para guardarlo en la variable de filas_antes

        # limpiar texto producto
        if "producto" in df.columns:
            df["producto"] = clean_text(df["producto"]) 
        #esta condicional dice que si encuentra producto procede hacer lo siguiente

        # CANASTA BASICA #en la columna producto crea esa lista tal cual como se le indico 
        CANASTA_BASICA = [
            "ARROZ",
            "FRIJOL",
            "LECHE",
            "HUEVO",
            "AZUCAR",
            "ACEITE",
            "PAN",
            "TORTILLA"
        ]

        if "producto" in df.columns:
            df = df[df["producto"].isin(CANASTA_BASICA)] 
            # .isin verifica si los elementos de una columna o DataFrame existen 
            # dentro de una lista específica para despues proceder a guardar la lista creada anteriormente

        # limpiar precio
        if "precio" in df.columns: # el df.columns es la variable
            # de todas la columnas por lo cual se especifica cual es la que se le va hacer modificaciones
            df["precio"] = df["precio"].apply(clean_price) #se aplica la funcion de cambiar formato a float
            df = df[df["precio"] <= 1000] # guarda los precios mas bajos y elimina los mas altos
    
        filas_despues = len(df) # muestra el conteo de filas procesadas despues de la limpieza

        print("Filas antes:", filas_antes)
        print("Filas después:", filas_despues) # muestra  los resultados de los 2 procesos

        print("\n--- INFO GENERAL PROFECO ---")
        df.info() # muestra el total de columnas y filas antes de procesar y despues de procesar 

    # print("\n--- MUESTRA PROFECO LIMPIO ---")
    # print(df.head(10).to_string())

        if "precio" in df.columns: #condicional que indica que encuentre la columna precio
            
            print("\n--- INFO PRECIOS ---")
            print(df["precio"].describe()) # la columna precio y lo muestra en consola

        output = PROCESSED_PATH / "profeco_clean.csv" #se guarda el archivo con los datos procesados
        df.to_csv(output, index=False, encoding="utf-8-sig") #se le pone el utf-8 para que 
        #no tenga conflictos con las tildes

        print(" Guardado:", output) #indica que se guardo de forma correcta



    # MAIN ETL (BUSQUEDA RECURSIVA)


    

    print("\nBuscando CSV en:", RAW_PATH) #indica que va a buscar en la ruta que se le dio

        # BUSCAR TODOS LOS CSV RECURSIVAMENTE
    files = list(RAW_PATH.rglob("*.csv"))  # comienza a enlistar 
        #la busqueda de archivos csv y los guarda en la variable files (los csv que vaya encontrando)

    if not files: # condicional en caso de que no encuentre csv
            print(" No hay CSV") #muestra este mensaje
            return # finaliza el ciclo de busqueda

    airbnb_files = [] #se crea lista vacia para almacenar el o los archivos que encuentre
    profeco_files = []

    for f in files: #ciclo para files usando f solo para cada paso del ciclo 

        path_str = str(f).lower() #aca se demuestra que f es solo para funciones en este ciclo
            # lo que hace aca es que todo dato string que este en mayuscula pasa a minuscula


            # ignorar diccionario
        if "diccionario" in path_str:
            #condición que verifica si la palabra específica "diccionario" 
            #está contenida dentro de una variable de texto llamada path_str.
                
            continue # Si encuentra la palabra 'diccionario' en esta ruta, 
            #la ignora y pasa a la siguiente".
            

        if "airbnb" in path_str or "listing" in path_str:#la condicion hace que
            # si la palabra airbnb o listing están presentes en la variable path_str
            #se agrega a una lista llamada airbnb_files
                airbnb_files.append(f) # con append se agrega los archivos enlistados

        elif "profeco" in path_str or "2025" in path_str: 
            # segunda condicion Si la primera condición (Airbnb) 
            # #no se cumplió, se revisa esta.
                profeco_files.append(f) # con append se agrega los archivos enlistados

        # AIRBNB
    for f in airbnb_files: # condicional para airbnb_files
            #nuevamente se crea con ciclo for y se le asigna la f 
            #igual que la anterior 
            process_airbnb(f) # se usa esa f porque ahi se agrego airbnb

        # PROFECO (TODOS JUNTOS)
    if profeco_files: #condicional  que indica que si la variable 
            #guardo uno o varios archivos en profeco
            process_profeco(profeco_files) # lo verifica con la funcion process_profeco
    else:
            print("No se encontraron archivos Profeco") #caso contrario arroja el mensaje



    # RUN

if __name__ == "__main__":
    main() #esta condicion indica que se ejecute todo cuando se decida ejecutar
        #si se quita no se va a ejecutar
