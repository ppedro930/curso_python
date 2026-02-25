usuario_raw = "         anGEL rOdriGuez Altamarina"  # variable tipo string

nombre_limpio = usuario_raw.strip().title()

usuario_minusculas = usuario_raw.strip().lower()
usuario_mayusculas = usuario_raw.strip().upper()

#print(f"Usuario original: '{usuario_raw}'")
#print(f"Usuario limpio: '{nombre_limpio}'")
#print(f"Usuario en minusculas: '{usuario_minusculas}'")
#print(f"Usuario en mayusculas: '{usuario_mayusculas}'")
#print(f"usuario minuscula sin strip: '{usuario_raw.lower()}'")

precio = "1500.5"
impuesto = 1.16

# total = precio * impuesto
total_2 =precio + "100"

concatenar = "banana" + " de" " chocolate"

# print(f"El total sin conversion: {total}")
print(f"El total con concatenAacion: {total_2}")

print(f"concatenacion de strings: {concatenar}")

print (f"Tipo de dato de precio: {type(precio)} y tipo de dato de impuesto: {type(impuesto)}")