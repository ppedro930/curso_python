import pandas   as pd
import numpy    as np

df = pd.read_csv("Superstore Sales Dataset.csv")

'''formas de definir funciones o declarar

def y lambda

def sera funcion reutilizable 
lambda: funcion unica y desechable

las funciones lambda no deberia tener logica compleja 

si usas lambda mas de 3 veces es conveniente usar funciones def (ya que lambda se usa solo 2 o 3 veces)

'''
def calcular_bono_limpio(valor):
    try:
        umbral = 100
        float(valor)
        tasa = 0.1
        if valor > umbral:
            return valor * tasa
            return 0
    except Exception:
        return None
df['Resultado_bono'] = df['Sales'].apply(calcular_bono_limpio)



'''1 - limpieza de texto (Extraccion)
a veces las columnas de id tienen codigos que necesitamos separar 
suponiendo que el order id tiene formato "CA-2017-152-125369"'''

#df['Order_Region'] = df['Order ID'].str.split('-').str[0]
#df['Order_Year']   = df['Order ID'].str.split('-').str[1]
#df['Order_Code']   = df['Order ID'].str.split('-').str[3]


#print(
 #   df[['Order ID', 'Order_Region', 'Order_Year']])


df['Market_code'] = df['Order ID'].apply(lambda ID: ID[:2]) # esto es solo para 1 columna


'''2 imagina que solo los productos de la categoria "Technology" 
tienen un impuesto especial del 15% sobre el precio de venta'''

df['Tax_amount'] = df.apply(lambda fila: fila['Sales'] * 0.15 if fila['Category'] == 'Technology' else 0, axis=1) #  esto es para varias columnas del dataframe (df.apply)

# df['columna especificada']
'''df['Tax_amount'] = np.where(
    df['Category'] == 'Technology',
    df['Sales'] * 0.15,
    0
)'''

print(df[['Category', 'Sales', 'Tax_amount']].head(10))


'''3 - quieres crear una etiqueta amigable para una grafica que combine la ciudad y el estado

reto: crea una columna Location_Full que combine las columnas City y State en el formato "Ciudad, Estado"
'''

lf = df['Location_Full'] = df.apply(lambda locat: f"{locat['State']}", axis=1)


print(lf) 


'''****************************'''

nombre = "Juan Perez"

slice_1 = nombre[:4]
slice_ = nombre[:]

print(slice_1, slice_2)


