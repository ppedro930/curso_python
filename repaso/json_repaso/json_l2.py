import json

with open('users.json', 'r', encoding='utf-8') as archivo:
    usuarios = json.load(archivo)
#print(f"tipo de dato salida {type(usuarios)}")

primer_usuario= usuarios[0]

nombre= primer_usuario['name']
correo = primer_usuario['email']

# print(f"usuario seleccionado: {nombre}")
# print(f"correo {correo}")
# print("-"*50)

caja_empresa = primer_usuario['company']
#print(f"contenido de la caja {caja_empresa}\n")

catch_phrase = primer_usuario['company']['catchPhrase']
# print(f"{nombre} tiene una catchPhrase que dice  {catch_phrase} ")

#print("-"*50)

direccion = primer_usuario['address']
geolocalizacion = direccion['geo']
latitud = geolocalizacion['lat']
longitud =primer_usuario['address']['geo']['lng']

#print(f"latitud exacta de {nombre} es: {latitud} con longitud {longitud}")

print("-"*50)

for u in usuarios:
    nombre_user = u['name']
    ciudad_actual = u['address']['city']
#    print(f"    - {nombre_user} vive en {ciudad_actual}")


