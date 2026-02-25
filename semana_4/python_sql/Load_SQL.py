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
    data_airbnb= pd.read_csv('airbnb_cdmx_limpio.csv')

    cadena_postgres = f'postgresql://{usuario}:{psw}@{host}:{puerto}/{database_name}'
    motor_postgres = create_engine(cadena_postgres)

    print('subiendo tabla principal a postgres')
    data_airbnb.to_sql('airbnb_cdmx_1', motor_postgres, if_exists='replace', index=False)

    print(f'carga exitosa{len(data_airbnb)} registros guardados en el servidor')

except Exception as e:
    print(f"error en la carga de postgreSQL {e}")

    




