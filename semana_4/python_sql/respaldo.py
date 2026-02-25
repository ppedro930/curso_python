import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

print(f"buscando credenciales...")

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_env = os.path.join(ruta_actual,'..','..','.env')

load_dotenv(dotenv_path=ruta_env)

usuario = os.getenv('DB_USER')
psw =os.getenv('DB_PASS')
host=os.getenv('DB_HOST')
puerto=os.getenv('PORT')
database_name=os.getenv('DB_NAME')

if not usuario:
    print("alerta no se encontro el archivo .env o esta vacio")
else:
    print("credenciales cargadas")
try:
    cadena_postgres = f'postgresql://{usuario}:{psw}@{host}:{puerto}/{database_name}'
    motor_postgres = create_engine(cadena_postgres)

    print("ejecutando query en postgreSQL")
    query = """
    SELECT
        neighbourhood_cleansed AS barrio,
        room_type AS tipo_cuarto,
        AVG(price) AS precio_promedio
    FROM airbnb_cdmx_1
    WHERE price IS NOT NULL
    GROUP BY neighbourhood_cleansed, room_Type
    HAVING AVG(price) >1500

    """
    df_resumen = pd.read_sql_query(query, motor_postgres)

    print("Pivoteando datos en pandas")
    tabla_resumen = df_resumen.pivot_table(
        index='barrio',
        columns='tipo_cuarto',
        values='precio_promedio',
        fill_value=0

    ).round(2).reset_index()

    print("mostrando resumen")
    print(tabla_resumen.head())

    print("\n generando archivo db...")
    motor_sqlite = create_engine('sqlite:///Reporte_directo.db')

    tabla_resumen.to_sql('resumen_precios_barrio', motor_sqlite, if_exists='replace', index=False)

    print("pipeline completo! se creo el archivo Reporte_directo.db directo a tu carpeta")

except Exception as e:
    print(f"error en proceso {e}")



