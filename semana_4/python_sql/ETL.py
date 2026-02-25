import pandas as pd
import numpy as np

print ("iniciando procesos ETL")

airbnb = pd.read_csv('listings.csv')

print(f"datos originales cargados: {airbnb.shape[0]} filas y {airbnb.shape[1]} columnas")

#print(f"\nInfo general: {airbnb.info()}")  #comentario debig

#columnas con todos los valores null:
#license, calendar_updated, neighbourhood_group_cleansed

columnas_to_drop = ['license', 'calendar_updated', 'neighbourhood_group_cleansed']

airbnb = airbnb[[col for col in airbnb.columns if col not in columnas_to_drop]] #lista comprension

airbnb = airbnb.drop_duplicates() #eliminar duplicados

#print(f"\nInfo general despues de drop: {airbnb.info()}")  #comentario debug

print(f"columna host_since: {airbnb['host_since'].head()}")

cols_texto = airbnb.select_dtypes(include=['object','string']).columns
airbnb[cols_texto] = airbnb[cols_texto].apply(lambda x: x.str.lower().str.strip())

print(f"columna price:{airbnb['price'].head()}")

#eliminar signos de pesos y comas para la columna price

if 'price' in airbnb.columns:

    airbnb['price'] =airbnb['price'].astype(str).replace(r'[\$,]', '', regex=True)

    airbnb['price'] =pd.to_numeric(airbnb['price'], errors='coerce')

#print(f"columna price \n{airbnb['price'].head()}")

#print(f"columnas de interes {airbnb[['host_since','last_review']]}")

columnas_fecha = ['host_since','last_review']

# ciclo for para convertir a formato fecha

for col_dt in columnas_fecha:
    if col_dt in  airbnb.columns:
        airbnb[col_dt]= pd.to_datetime(airbnb[col_dt],errors='coerce')

#condicional for para calcular cuanto tiempo tiene el host el airbnb desde la fecha que se ejecuta el script

if 'host_since' in airbnb.columns:
    fecha_actual = pd.to_datetime('today')
    airbnb['antiguedad_host'] = np.floor ((fecha_actual-airbnb['host_since']).dt.days / 365.25)

#print(f"columna creada \n {airbnb[['host_since','antiguedad_host']].tail(10)}")

#condicional para saber clasificar entre el tipo_viajes y accommodate entre solos pareja y grupo fiesta

if 'accommodates' in airbnb.columns:
    airbnb['tipo_viaje'] = airbnb['accommodates'].apply(
        lambda x: 'solos/pareja' if x<=2 else (
            'familia pequeña' if x<=5 else 'grupo/fiesta'
        )
    )

#print(f"columna creada: \n {airbnb[['accommodates','tipo_viaje']].head(10)}")


# esta condicional es para clasificar los espacios de acuerdo a su demanda del año


if 'availability_365' in airbnb.columns:

    airbnb.loc[airbnb['availability_365'] < 50, 'nivel demanda'] = 'alta demanda'
    airbnb.loc[(airbnb['availability_365'] >= 50) & (airbnb['availability_365'] < 200), 'nivel demanda'] = 'demanda media'
    airbnb.loc[airbnb['availability_365'] > 200,'nivel demanda'] = 'baja demanda'
#print(f"columna de demanda: \n {airbnb.loc[airbnb['nivel demanda'] == 'alta demanda'].tail(5)}" )


#rellenar valores nulos con una mediana

if 'bedrooms' in airbnb.columns:
    airbnb['bedrooms'] = airbnb['bedrooms'].fillna(airbnb['bedrooms'].median())

#rellenar valores nulos del precio pues no hay manera de inferir directamente
if 'price' in airbnb.columns:
    valores_drop = airbnb['price'].isna().sum()
    airbnb = airbnb.dropna(subset=['price'])
    print(f"se eliminaron {valores_drop} filas que no tenian precio")

# se deben eliminar las columnas con mas de 1000 valores unicos pues no 
# #representan categorias unicas mas bien son valores inservibles

cols_numericas = airbnb.select_dtypes(include='number').columns
columnas_fecha = airbnb.select_dtypes(include='datetime64[ns]').columns
cols_texto_real = airbnb.select_dtypes(include=['object','string']).columns
unicos_texto = airbnb[cols_texto_real].nunique()

# print(unicos_texto)

#print(f"columna de amenidades{airbnb['amenities'].head()}") #clasificar con ia esta columna para encontrar grupos

cols_texto_save = unicos_texto[unicos_texto < 1000].index
cols_finales = list(cols_numericas) + list(columnas_fecha) + list(cols_texto_save)
airbnb_limpio = airbnb[cols_finales].copy()

airbnb_limpio.to_csv('airbnb_cdmx_limpio.csv', index=False)
print(f"archivo guardado con {airbnb_limpio.shape[0]} filas y {airbnb_limpio.shape[1]} columnas")

#print(airbnb_limpio.info())
if 'estimated_revenue_l365d' in airbnb_limpio.columns and 'neighbourhood_cleansed' in airbnb_limpio.columns:
    promedio_real= airbnb_limpio.groupby('neighbourhood_cleansed')['estimated_revenue_l365d'].mean().reset_index()
    promedio_global= airbnb_limpio['estimated_revenue_l365d'].mean()

    promedio_real['revenue_target']= promedio_global*1.15

    metas = promedio_real[['neighbourhood_cleansed', 'revenue_target']]
    metas.to_excel('metas_26.xlsx', index=False)
    print('archivo guardado')


