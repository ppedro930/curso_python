import json

with open('users.json', 'r', encoding='utf-8') as archivo:
    usuarios = json.load(archivo)



print(f"radar activado: {len(usuarios)} objetos en la mira\n")

habitantes_gwenborough = []

for u in usuarios:
    # entramos a la caja 'address' y sacamos city
    ciudad= u['address']['city']

    if ciudad == "Gwenborough":
        habitantes_gwenborough.append(u['name'])
print(f"usuarios que viven en Gwenborough: {habitantes_gwenborough}")

print("-"*50)

empleados_romaguera = []

for u in usuarios:
    empresa = u['company']['name']

    if "Romaguera" in empresa:
        empleados_romaguera.append(u['name'])
print(f"empleados de las empresas romaguera {empleados_romaguera}")
print("-"*50)

norteños = []
sureños =[]

for u in usuarios:
    latitud_texto = u['address']['geo']['lat']
    latitud_numero = float(latitud_texto)

    if latitud_numero < 0:
        sureños.append(u['name'])
    else:
        norteños.append(u['name'])

print("distribucion geografica")
print(f"  - hemisferio sur (lat < 0): {len(sureños)} usuarios")
print(f"  - hemisferio norte (lat >= 0): {len(norteños)} usuarios")



