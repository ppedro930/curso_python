import pandas as pd
import numpy as np


#PRIMERO SE MANDA A TRAER EL ARCHIVO QUE SE VA A LEER 
# #primero se define la funcion que recibe la ruta del archivo 
# y se intenta #cargar el archivo con el comando de la libreria pandas para que lo identifique, en este caso con
#  pd.read_csv, y en caso de que el archivo no se encuentre aparece 
# el mensaje de excepcion FileNotFoundError imprimiendo un mensaje de error, 
# y retornando None para indicsr que no se pudo cargar el archivo


#def leer_csv(ubicacion_del_archivo):
 #   try:
  #      return pd.read_csv(ubicacion_del_archivo)
   # except FileNotFoundError:
    #    print("Aca no esta el archivo buscalo bien revisa la ruta")
     #   return None



# PROCESO PRINCIPAL
# en este apartado primeramente se revisan los datos con sus tipos de datos 
# originales indicando cuales cuales son los que hay que modificar en caso de ser cadena 
# string y toque cambiarlo
#ya sea a fecha, numerico, booleano, etc.


#-----------------------experimentar sin mandar a traer el archivo

df = pd.read_csv('airbnb.csv')

print("\nInformación original-----campos por default en su archivo csv (estos son sus formatos antiguos)") 

info = df.info()

print(info)

#---------------------con este se usa try

#df = leer_csv('airbnb.csv')

#print("\nInformación original-----campos por default en su archivo csv (estos son sus formatos antiguos)") 
#print(df.info())


# VALIDACIÓN DE DATAFRAME
#esto es para identificar cuales son los campos y los registros
#cuales son sus tipos de datos y cuales de ellos poseen campos vacios

def validar_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("aca no hay ni campos ni registros de excel o sql etc... estructurados " \
        "en dataframe o por lo menos no los he reconocido")
    return True


# LIMPIEZA DE FECHAS
# En este paso se identifican las columnas que deberían tener formato de fecha. 
# # Cada una se convierte a tipo datetime usando pd.to_datetime. 
# la palabra coerce es para que obligatoriamente lo cambie especificando su formato correcto 
# # Si algún valor no puede convertirse, se reemplaza por NaT (valor nulo de fechas).

def este_cambia_fechas(df):
    columnas_que_encontre_de_fechas_para_cambiar_su_formato = ['last_scraped','calendar_last_scraped','first_review','last_review']

    for col in columnas_que_encontre_de_fechas_para_cambiar_su_formato:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df


# LIMPIEZA DE PORCENTAJES
# Aquí se limpian las columnas que vienen como porcentaje en texto (ej: "95%"). 
# # Primero se elimina el símbolo %, luego se convierten a números 
# # y finalmente se dividen entre 100 para trabajar con valores decimales.

def este_modifica_porcentajes(df):
    columnas = ['host_response_rate', 'host_acceptance_rate']

    for col in columnas:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace('%', '', regex=False).replace('nan', np.nan).astype(float)/ 100)
    return df


# LIMPIEZA DE PRECIO

# En este paso se limpia la columna price. # Se eliminan símbolos como el signo $ y las comas, 
# # y después se convierte el valor a tipo numérico (float) # para poder hacer cálculos correctamente.

def campo_precio_para_cambiarlo(df):
    if 'price' in df.columns:
        df['price'] = (df['price'].astype(str).str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False).astype(float))
    return df


# DISPONIBILIDAD (BOOLEANO)

# Se crea una nueva columna booleana llamada has_availability. 
# # Si availability_365 es mayor que 0, se considera que el alojamiento 
# # tiene disponibilidad y se asigna True, de lo contrario False.

def crear_disponibilidad(df):
    if 'availability_365' in df.columns: df['has_availability'] = df['availability_365'] > 0
    return df

# LIMPIEZA DE BOOLEANOS

# En este bloque se convierten columnas que representan valores lógicos 
# # (sí / no, verdadero / falso) al tipo booleano de Python. 
# # Esto facilita filtros y análisis posteriores.

def este_cambia_booleanos(df):
    columnas = ['host_is_superhost','host_has_profile_pic','host_identity_verified','instant_bookable']

    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    return df


# FILTRAR PRECIOS VÁLIDOS

# Aquí se filtran los registros dejando únicamente aquellos 
# # cuyo precio sea mayor a 0, eliminando valores inválidos # o que no sirven para el análisis.

def filtrar_precios(df):
    if 'price' in df.columns:
        return df.loc[df['price'] > 0]
    return df


# INFERENCIA CON APPLY + LAMBDA 
    #Esta función infiere una nueva columna categórica
    #a partir del precio usando apply + lambda.
    



def categorizar_precio(df):
    
    if 'price' in df.columns:
        df['price_category'] = df['price'].apply(
            lambda x: 'Bajo' if x < 50 else 'Medio' if x < 150 else 'Alto'
        )
    return df


# USO DE SLICES EN TEXTO 
#Se extraen los primeros 3 caracteres del host_name
#  usando slicing de strings.

def extraer_host_prefix(df):
    
    if 'host_name' in df.columns:
        df['host_prefix'] = df['host_name'].astype(str).str.slice(0, 3)
    return df


# RESUMEN CON GROUPBY
def resumen_precios(df):
    if 'room_type' in df.columns:
        return df.groupby('room_type')['price'].mean()




try:
    validar_dataframe(df)

    

    df = este_cambia_fechas(df)
    df = este_modifica_porcentajes(df)
    df = campo_precio_para_cambiarlo(df)
    df = crear_disponibilidad(df)
    df = este_cambia_booleanos(df)
    df = filtrar_precios(df)
    df = categorizar_precio(df)
    df = extraer_host_prefix(df)

    # VARIABLES TEMPORALES
    if 'last_scraped' in df.columns:
        df['Mes'] = df['last_scraped'].dt.month
        df['Hora'] = df['last_scraped'].dt.hour
        df['Dia_Semana'] = df['last_scraped'].dt.day_name()
        df['ISO_Year'] = df['last_scraped'].dt.isocalendar().year
        df['ISO_Day'] = df['last_scraped'].dt.isocalendar().day

    print("\nInformación después de la limpieza-----aca se muestran los datos ya modificados despues de hacer el try ")
    print(df.info())

    print("\nPrecio promedio por tipo de habitación")
    print(resumen_precios(df))

    df.to_csv('airbnb_modificado_tal_cual.csv', index=False)
    print("\nArchivo 'airbnb_modificado_tal_cual.csv' guardado correctamente")

except TypeError as e:
    print("Error:", e)
