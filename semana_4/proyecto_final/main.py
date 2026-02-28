from src.etl_process import main as etl_main # Desde el la carpeta
#src, ingresa al archivo etl_process.py, toma la función principal (main)
# y renómbrala localmente como etl_main.
from src.train_model import main as train_main
from src.ai_agent import main as ai_main
from src.db_ingestion import main as db_main


def main():
    print("Iniciando Pipeline proyecto_final...\n") # si logra todo lo anterior

    try:
        print("1 Ejecutando ETL...")
        etl_main()

        print("2 Entrenando modelo y clustering...")
        train_main()

        print("3 Generando reporte con IA...")
        ai_main()

        print("4 Cargando datos a la base de datos...")
        db_main()

        print("\n Pipeline ejecutado exitosamente.")

    except Exception as e:
        print(f"\n Error en el pipeline: {e}")


if __name__ == "__main__":
    main()
