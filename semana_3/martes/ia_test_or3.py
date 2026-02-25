import time
from motor_ia import analizar_sentimiento

#en motor ia añadir funcion que convierte a imagen y mandar a llamar ia test 

textos = [
    "El material del curso es bueno",
    "mi mama hizo spagguetincon catsup"
    "el archivo de excel falla"
]

print("\n iniciando test de modulacion...")
for t in textos:
    resultado, tiempo, t_in, t_out, id_modelo = analizar_sentimiento(t)

    if "ERROR" in resultado:
        print(f"!!!!! {resultado}")
    else:
        print(f"texto: {t}")
        print(f"sentimiento segun gemini: {resultado}")
        print(f"modelo utilizado es: {id_modelo}")
        print(f"sentimiento: {resultado} | tiempo {tiempo} segundos | tokens entrada {t_in} | tokens salida {t_out}")
        
        
        print("-" * 40)

        time.sleep(4)  # Pausa de 1 segundo entre cada análisis para evitar saturar la API

print("test de modulacion finalizado.")