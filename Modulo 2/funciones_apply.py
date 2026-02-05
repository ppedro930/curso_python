import  pandas as pd
import numpy as np

df = pd.read_csv("Superstore Sales Dataset.csv")

#df.apply(function)  # Suma de cada columna

df['City_length'] = df['City'].apply(len)

#crear columna nueva con la longitud del nombre de la ciudad

#df['Nueva columna']

#print(df['City_length'])

df ['Sales_String'] = df['Sales'].apply(str)

#print(df['Sales'].describe(include=['object',"string"], []))

df['Raiz Ventas'] = df['Sales'].apply(np.sqrt)

print(df['Raiz Ventas'].head(15))


'''
1.- Normalización Logarítmica
En análisis de datos, las ventas suelen tener valores muy dispersos. 
Una técnica común es aplicar el logaritmo natural para "suavizar" los datos.

2.- Redondeo al Entero Superior (Techo)
Imagina que para logística necesitas calcular cuántas cajas usar, y cualquier decimal requiere una caja extra.

3.- En el dataset de Superstore, la columna Profit (Ganancias) puede tener valores negativos. 
Queremos saber rápidamente si la operación fue positiva, negativa o cero.

Reto: Crea una columna llamada Profit_Sign usando la función np.sign. 
Esta función devuelve 1 si es positivo, -1 si es negativo y 0 si es cero.

4.- Valores Absolutos para Análisis de Impacto
A veces no importa si perdimos o ganamos, sino la magnitud del movimiento de dinero.

5.- Para fines contables conservadores, quieres ignorar los decimales de las ventas y 
quedarte solo con la parte entera hacia abajo.

6.- Transformación Logarítmica SeguraEl logaritmo natural falla si el valor es 0. 
NumPy tiene una función llamada np.log1p que calcula $log(1 + x)$, 
lo cual es más estable para datos de ventas.
Reto: Aplica np.log1p a la columna Sales y guarda el resultado en Sales_Log_Stable.

7.- ndo la lógica es muy específica, lo mejor es definir una función con def y luego pasarla por nombre al apply.

Reto: Crea una función llamada calcular_iva que multiplique el valor por 0.16. Luego, aplícala a la columna Sales.
'''




# 1 especificar en sales a traves de guion bajo que lo va hacer en logaritmo y luego usar libreria numpycon tipo de dato 
# log y df para que lea el archivo 

df['Sales_Log'] =df['Sales'].apply(np.log)
#ninguna funcion acepta dataframes como argumento

# 2. Redondeo al Entero Superior (Techo)

df['Logistica'] = df['Sales'] .apply(np.ceil)


# 3. Signo de las Ganancias

df['Profit_Sign'] = df['Sales'] .apply(np.sign)


# 4. Valores Absolutos del Profit

df['Abs'] = df['Abs'].apply(np.abs)


# 5. Parte Entera hacia Abajo (Piso)


df['Sales_Floor'] = df['Sales'].apply(np.floor)


# 6. Transformación Logarítmica Segura

df['Log_Stable'] = df['Sales'].apply(np.log1p)


# 7. Función personalizada con apply

def calcular_iva(valor):
    return valor * 0.16

df['IVA'] = df['Sales'].apply(calcular_iva)


# Verificación rápida

print(df[['Sales', 'Sales_Log', 'Sales_Ceiling', 'Sales_Floor',
          'Sales_Log_Stable', 'Profit', 'Profit_Sign', 'Profit_Abs', 'IVA']].head())


'''imprimir valores 

reto:usar loc o iloc usar filtros especificos'''
