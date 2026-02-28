texto_crudo = "el cod limpio es buen cod, y eso es arte."

texto_limpio = texto_crudo.lower().replace(",","").replace(".","")
#print(texto_limpio)

lista_palabras = texto_limpio.split()

registro_palabras = {}

print(lista_palabras)

for indice,palabra in enumerate(lista_palabras):
    if palabra not in registro_palabras:
        registro_palabras[palabra] = {"frecuencia":1,"pocisiones":(indice,)}
    else:
        registro_palabras[palabra]["frecuencia"] += 1

        registro_palabras[palabra]["pocisiones"] += (indice,)

print(f"texto analizado es {texto_crudo}")
print(f"{'palabra':<10} | {'frecuencia':<10} | {'indices'}")
print("-"*50)

for palabra,datos in registro_palabras.items():
    freq = datos["frecuencia"]
    pos = datos["pocisiones"]

    print(f"{palabra:>10} | {freq:>10} | {pos}")
