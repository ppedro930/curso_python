import time
from motor_ia import analizar_imagen_bin, analizar_imagen_cloud, analizar_sentimiento

print("\nIniciando test de modulación...")

ruta_imagen = "actividad.jpg"

#  TEST BINARIO 
print("\n--- TEST BINARIO ---")

with open(ruta_imagen, "rb") as f:
    img_bytes = f.read()

resultado, duracion, t_in, t_out, nombre_real_modelo = analizar_imagen_bin(img_bytes)

if "Error" in resultado:
    print("!!!!!", resultado)
else:
    print("modelo:", nombre_real_modelo)
    print("resultado:", resultado)
    print("tiempo:", duracion, "s")
    print("tokens entrada:", t_in)
    print("tokens salida:", t_out)

time.sleep(3)


#  TEST CLOUD 
print("\n--- TEST CLOUD ---")

resultado, duracion, t_in, t_out, nombre_real_modelo = analizar_imagen_cloud(ruta_imagen)

if "Error" in resultado:
    print("!!!!!", resultado)
else:
    print("modelo:", nombre_real_modelo)
    print("resultado:", resultado)
    print("tiempo:", duracion, "s")
    print("tokens entrada:", t_in)
    print("tokens salida:", t_out)

    time.sleep(4)
print("\ntest de modulación finalizado.")


#  ANALIZAR SENTIMIENTO



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