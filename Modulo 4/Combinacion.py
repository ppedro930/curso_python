import os # operativo system
import glob
import pandas as pd

from datetime import datetime
from datetime import date

'''
estas librerias funcionan para navegar entre archivos 

'''
donde_estoy = os.getcwd() # me dice donde estoy ubicado la ruta actual donde se ejecuta el codigo

print(donde_estoy)

ruta_carpeta = "./Sales_Data"  # el./sales data es la carpeta donde se encuentran los archivos csv, el 
#punto es para decir que esta en la misma carpeta donde se ejecuta el codigo

archivos_csv = glob.glob(os.path.join(ruta_carpeta, "*.csv")) # glob es una libreria que me permite buscar archivos con un patron especifico, en este caso todos los archivos con extension .csv en la carpeta Sales_Data

cantidad_archivos = len(archivos_csv) # len me da la cantidad de archivos encontrados

print(cantidad_archivos)
#print(archivos_csv)

lista_df =[]

for archivo in archivos_csv:

    df_mes = pd.read_csv(archivo) # pd.read_csv es una funcion de pandas que me permite leer un archivo csv y convertirlo en un dataframe
    lista_df.append(df_mes) # append es una funcion de las listas que me permite agregar un elemento al final de la lista

    lista_df.append(df_mes) # append es una funcion de las listas que me permite agregar un elemento al final de la lista
    print(f"Archivo {os.path.basename(archivo)} cargado correctamente") # f es para formatear la cadena de texto y mostrar el nombre del archivo que se cargo

df_anual = pd.concat(lista_df, ignore_index=True) # pd.concat es una funcion de pandas que me permite concatenar varios dataframes en uno solo, ignore_index=True es para resetear el indice del nuevo dataframe

print("----------datos unidos---------")
#print(df_anual.tail())
print(df_anual.info())

convertir = ['Quantity Ordered', 'Price Each'] # esto es para ver los valores únicos en la columna Item después de la limpieza
print(convertir)








df_anual ['Quantity Ordered'] = pd.to_numeric(df_anual['Quantity Ordered'], errors='coerce') 

df_anual['Price Each'] = pd.to_numeric(df_anual['Price Each'], errors='coerce') #lo convierte a float

df_anual['Order Date'] =  pd.to_datetime(df_anual['Order Date'], errors='coerce', format='%Y/%m/%d %H:%M') # convertir la fecha en su orden  con su hora




#df_anual['Order ID'] = pd.to_numeric(df_anual['Order ID'], errors='coerce')

df_anual['Order ID'] = (
    pd.to_numeric(df_anual['Order ID'], errors='coerce')
    .astype('Int64')
)

print("-----------------------------")

print(df_anual.info())

df_anual['Mes'] = df_anual['Order Date'] # crear una nueva columna llamada 
#mes que extrae el mes de la columna order date

ts = pd.to_datetime(df_anual['Order Date'], errors='coerce', format='%m/%d/%y %H:/M') # convertir la columna order date a formato de fecha y hora

print("---"*60)

print(df_anual.info()) # esto es para ver los valores únicos en la columna mes

df_anual['Mes'] = df_anual['Order Date'].dt.month # extraer el mes de la columna order date y guardarlo en la columna mes
df_anual['Hora'] = df_anual['Order Date'].dt.hour # extraer la hora de la columna order date y guardarlo en la columna hora
df_anual['Dia_Semana'] = df_anual['Order Date'].dt.day_name() # extraer el dia de la semana de la columna order date y guardarlo en la columna dia semana

df_anual['ISO_Year'] = df_anual['Order Date'].dt.isocalendar().year # extraer el año ISO de la columna order date y guardarlo en la columna ISO year
df_anual['ISO_Month'] = df_anual['Order Date'].dt.isocalendar().month # extraer el mes ISO de la columna order date y guardarlo en la columna ISO month
df_anual['ISO_Day'] = df_anual['Order Date'].dt.isocalendar().day # extraer el dia ISO de la columna order date y guardarlo en la columna ISO day

print("..."*60)
print(df_anual['Mes']) # esto es para ver los valores únicos en la columna mes

ventas_por_hora = df_anual.groupby('Hora').size() # agrupar por hora y contar la cantidad de ventas por hora
ventas_por_dia = df_anual.groupby(['Mes','Dia_Semana']).size() # agrupar por dia de la semana y contar la cantidad de ventas por dia de la semana

ventas_mes = df_anual.groupby('Mes').size() # agrupar por mes y contar la cantidad de ventas por mes

print(ventas_por_hora)
print(ventas_por_dia)
print(ventas_mes)

#transfomar las columnas Quantity Ordered y Price Each a tipo numerico
#y transformar la columna Order Date a tipo fecha



#darle formato a order date (dia mes año)
#convertir a enteros y no a float order id



