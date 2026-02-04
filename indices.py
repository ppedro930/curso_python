meses = ["Enero", "Febrero", "Marzo"]

# mes: Enero     Febrero     Marzo
# indice: 0         1          2

indice = 0

if indice < len(meses):
    print(f"El mes en el indice {indice} es: {meses[indice]}")
else:
    print(f"Error: el indice {indice} no existe. La lista tiene {len(meses)} elementos.")