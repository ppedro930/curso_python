import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_batch
import time

inicio = time.time()

print("🚀 INICIANDO CARGA POSTGRESQL PRO")



# BASE DIR


BASE_DIR = Path(__file__).resolve().parents[1] #ubicacion absoluta... parents[1] es la carpeta que está un nivel más arriba.

ENV_PATH = BASE_DIR / ".env" # indica donde esta el archivo de la conexion
AIRBNB_FILE = BASE_DIR / "data" / "clusters" / "airbnb_clustered.csv" #archivo a leer para procesar bd
PROFECO_FILE = BASE_DIR / "data" / "processed" / "profeco_clean.csv"  #archivo a leer para procesar bd



# ENV


load_dotenv(dotenv_path=ENV_PATH) # carga datos del .env

usuario = os.getenv('DB_USER')
psw = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
puerto = os.getenv('PORT')
database_name = os.getenv('DB_NAME') #se especifican para ver si coinciden... de ser asi se carga para conectar

if not usuario: #condicional por si algo en el env no coicide o si estan vacias las variables
    raise Exception("❌ .env no cargado")

print("✅ credenciales OK") # en caso que todo coincida bien... sale esto



# LEER CSV


print("📄 leyendo archivos...") 

df_airbnb = pd.read_csv(AIRBNB_FILE) # lectura de archivos para procesar lo necesario
df_profeco = pd.read_csv(PROFECO_FILE)

# normalizar nombres columnas PRO
df_airbnb.columns = df_airbnb.columns.str.lower().str.strip()
df_profeco.columns = df_profeco.columns.str.lower().str.strip() 
#.lower() pasa a mayusculas las columnas
#.str.strip() Elimina los espacios en blanco al principio y al final

print("Airbnb:", len(df_airbnb)) # hace el conteo de filas totales
print("Profeco:", len(df_profeco)) 



# LIMPIEZA NUMERICA


def to_num(col): #funcion que convierte a numerico la columna que se especifique
    return pd.to_numeric(col, errors="coerce").fillna(0)

# Airbnb
df_airbnb["price"] = to_num(df_airbnb.get("price"))
df_airbnb["minimum_nights"] = to_num(df_airbnb.get("minimum_nights"))
df_airbnb["cluster"] = to_num(df_airbnb.get("cluster"))
df_airbnb["latitude"] = to_num(df_airbnb.get("latitude"))
df_airbnb["longitude"] = to_num(df_airbnb.get("longitude"))

# Profeco
df_profeco["precio"] = to_num(df_profeco.get("precio"))
df_profeco["latitud"] = to_num(df_profeco.get("latitud"))
df_profeco["longitud"] = to_num(df_profeco.get("longitud"))



# CONEXION POSTGRES


conn = psycopg2.connect(
    dbname=database_name,
    user=usuario,
    password=psw,
    host=host,
    port=puerto
) # aca se le dan las variables del .env

cursor = conn.cursor() # .cursor() es una funcion para enviar comandos sql

print("🗄 conectado a PostgreSQL")



# CREAR TABLAS PRO conla funcion de execute para que realice la consulta


cursor.execute("""
CREATE TABLE IF NOT EXISTS airbnb (
    id BIGINT,
    name TEXT,
    neighbourhood TEXT,
    latitude REAL,
    longitude REAL,
    price REAL,
    minimum_nights INTEGER,
    cluster INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profeco (
    producto TEXT,
    municipio TEXT,
    latitud REAL,
    longitud REAL,
    precio REAL
)
""")

cursor.execute("TRUNCATE airbnb") 
#TRUNCATE es para eliminar de forma rápida y eficiente todos 
# los registros de una tabla, manteniendo 
# su estructura columnas, índices, restricciones intacta
cursor.execute("TRUNCATE profeco")



# PREPARAR DATOS MASIVOS


print("⚡ preparando Airbnb...")

datos_airbnb = [
(
    int(r.id) if pd.notna(r.id) else 0, 
    # "Si el ID existe, conviértelo a entero; si es un valor nulo (NaN), ponle un cero
    str(r.name) if pd.notna(r.name) else "",
    # "Si el nombre existe, conviértelo a string; si es un valor vacio, dejalo en balnco
    str(getattr(r,"neighbourhood_cleansed","")) , #lee y obtiene datos de neighbourhood
    float(r.latitude), #lee los datos tipo float para insertarlos despues
    float(r.longitude),
    float(r.price),
    int(r.minimum_nights),
    int(r.cluster)
)
for r in df_airbnb.itertuples()
]


print("⚡ preparando Profeco...")

datos_profeco = [
(
    str(r.producto) if pd.notna(r.producto) else "", # lee y si hay datos vacios asi se queda asi
    str(r.municipio) if pd.notna(r.municipio) else "",
    float(r.latitud),
    float(r.longitud),
    float(r.precio) #los lee para despues insertarlos
)
for r in df_profeco.itertuples()
]
#.itertuples() es para recorrer (iterar) las filas de un DataFrame de una manera mucho 
# más rápida y eficiente



# INSERT MASIVO ULTRA RAPIDO


print("⬆ insertando Airbnb...")
execute_batch(cursor, """
INSERT INTO airbnb 
(id,name,neighbourhood,latitude,longitude,price,minimum_nights,cluster)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""", datos_airbnb, page_size=10000) #

print("⬆ insertando Profeco...")
execute_batch(cursor, """
INSERT INTO profeco 
(producto,municipio,latitud,longitud,precio)
VALUES (%s,%s,%s,%s,%s)
""", datos_profeco, page_size=10000) #se ejecutan los comandos para que se inserten directo 
# en la bd postgres

conn.commit() # .commit() indica que lo que se hizo se guardo tal cual en la base de datos



# VALIDACION


cursor.execute("SELECT COUNT(*) FROM airbnb") # consulta para ver si las filas se insertaron
print("registros Airbnb:", cursor.fetchone()[0]) #resultado de la consulta

cursor.execute("SELECT COUNT(*) FROM profeco")
print("registros Profeco:", cursor.fetchone()[0])

cursor.close() #cierra consulta
conn.close()  #cierra conexion

print("BASE LISTA PARA POWER BI")

print("⏱ tiempo total:", round(time.time()-inicio,2),"seg")