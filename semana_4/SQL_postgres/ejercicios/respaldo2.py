import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

print(f"buscando credenciales...")

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_env = os.path.join(ruta_actual,'..','..','..','.env')

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
    i.billing_country AS pais,
    g.name AS genero,
    SUM(il.unit_price * il.quantity) AS total_dinero,
    COUNT(il.invoice_line_id) AS total_transacciones
FROM invoice i
JOIN invoice_line il ON i.invoice_id = il.invoice_id
JOIN track t ON il.track_id = t.track_id
JOIN genre g ON t.genre_id = g.genre_id
GROUP BY i.billing_country, g.name
ORDER BY pais ASC, total_dinero DESC;
    """
    df_resumen = pd.read_sql_query(query, motor_postgres)

    #print("Pivoteando datos en pandas")
    #tabla_resumen = df_resumen.pivot_table(
    #    index='nombre',
    #    columns='apellido',
    #    values='pais',
    #    fill_value=0

    

    #).round(2).reset_index()
    print("Pivoteando datos en pandas")
    tabla_resumen = df_resumen.sort_values(['pais','genero','total_dinero','total_transacciones'])

    print("mostrando resumen")
    print(tabla_resumen.head())

    #print("\n generando archivo CSV...")
    #tabla_resumen.to_csv("consulta7.csv", index=False, encoding="utf-8")
    #print("CSV creado correctamente")

    #print("\n generando archivo db...")
    #motor_sqlite = create_engine('sqlite:///consulta12.db')

    #print("\n generando archivo Excel...")
    #tabla_resumen.to_excel("consulta16.xlsx", index=False)
    #print("Excel creado correctamente")

    print("\n generando archivo TXT...")
    tabla_resumen.to_csv("consulta21.txt", index=False, sep="\t", encoding="utf-8-sig")
    print("TXT creado correctamente")

    #tabla_resumen.to_sql('consulta8', motor_sqlite,  if_exists='replace', index=False) #motor_sqlite, se agrega en sql

    




except Exception as e:
    print(f"error en proceso {e}")



