import pandas as pd

import numpy as np

'''
El proceso ETL es para extraer datos (Extract), transformarlos (Transform) y limpiarlos y finalmente cargarlos o compartirlos en algun lado
 (Load) '''

archivo = pd.read_csv('dirty_cafe_sales.csv')


info = archivo.info()
print(info)  #  esto es para ver Cuántas filas Cuántas columnas Si los datos son números o letras

print(archivo.isnull().sum()) # esto es para ver los valores nulos es decir (Cuántos espacios están vacíos) en cada columna

archivo['Item'] = archivo['Item'].str.strip().str.title() # esto es para eliminar los espacios en blanco al principio y al final de cada valor en la columna Item

item_unicos = archivo['Item'].unique() # esto es para ver qué productos existen y qué cosas se vendieron tambien los campos unknown y error
print(item_unicos)  # esto es para ver qué productos existen y qué cosas se vendieron tambien los campos unknown y error

spent_unicos = archivo['Total Spent'].unique()
print(spent_unicos) # Aquí vemos los precios, pero algunos están mal escritos Por eso luego se va a arreglar

columna_numericas = ['Total Spent', 'Price Per Unit', 'Quantity']

for col in columna_numericas:
   archivo[col] = pd.to_numeric(archivo[col], errors='coerce')

print(archivo[columna_numericas].dtypes) # esto es para ver si ya se convirtieron a números las columnas que queríamos

basura = ['Unknown', 'Error']
archivo['Item'] = archivo['Item'].replace(basura, pd.NA)

print(archivo['Item'].isnull().sum())  # esto es para ver cuántos valores nulos hay en la columna Item después de reemplazar

pagos_unicos = archivo['Payment Method'].unique()
print(pagos_unicos)  # esto es para ver los métodos de pago únicos

moda_pago_unico = archivo['Payment Method'].mode()[0]
archivo['Payment Method'] = archivo['Payment Method'].fillna(moda_pago_unico) # esto es para llenar los valores nulos con la moda es decir 
#si la mayor parte compra con tarjeta se llena de esa manera

gasto_unico = archivo['Total Spent'].unique()
print(gasto_unico)

#Total Spent = Price Per Unit * Quantity 

mask = archivo['Total Spent'].isna() & archivo['Quantity'].notna() & archivo['Price Per Unit'].notna()

#devolvera un 1 (true) si cumple la condicion y 0 (false) si no la cumple

#print ("---mascara---")

print(mask.apply(int))  # esto es para ver la máscara convertida a enteros

archivo.loc[mask, 'Total Spent'] = archivo['Quantity'] * archivo[ 'Price Per Unit']

archivo['Transaction Date'] = pd.to_datetime(archivo['Transaction Date'], errors='coerce') # esto es para convertir la columna de fecha a formato de fecha y hora y datos vacios en nan

columnas_de_interes = [ 'Item', 'Quantity', 'Price Per Unit',  'Total Spent', 'Payment Method', 'Transaction Date']

print("columnas ultimo despues de limpieza----------------------------------------------")
print(archivo[columnas_de_interes].info()) # esto es para ver las primeras filas de las columnas que nos interesan

#print(archivo.isnull().sum())

print("--- valores unicoooooooooooooooos---")

print(archivo[columnas_de_interes].nunique()) # esto es para ver los valores únicos en la columna Item después de la limpieza
print("---------------------- valores nulossssssssssssssssssssssssssssss---")
print(archivo[columnas_de_interes].isnull().sum()) # esto es para ver las primeras filas de las columnas que nos interesan

#tareaaaaaaaaaa

#reducir los NAN de item tomando como base el valor de 'Price Per Unit'

#al acabar de limpiar... hacer un comando  archivo.to_csv('ventas de cafe limpio.csv', index=False)  


