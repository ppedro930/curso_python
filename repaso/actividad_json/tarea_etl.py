import json

with open('ventas.json', 'r', encoding='utf-8') as archivo:
    ordenes_compra = json.load(archivo)

#usuarios_limpios = []
print(f"existen: {len(ordenes_compra)} ordenes de compra\n")

ordenes_compra = []

for o in ordenes_compra:
    
    nombre_cliente = o['nombre']
    producto = o['producto']
    
    print(f"Cliente: {nombre_cliente} compró: {producto}")
