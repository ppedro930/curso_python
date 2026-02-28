import json  

with open('ventas.json', 'r', encoding='utf-8') as archivo:
    ordenes_compra = json.load(archivo)

print(f"Existen: {len(ordenes_compra)} órdenes de compra\n")

orden_compra=[]

for i in range(len(ordenes_compra)): #cuenta la lista completa
    if i == 1: # si el indice 1 existe
        orden = ordenes_compra[i] # lo selecciona y lo guarda
        
        orden = {
        "nombre": orden['cliente']['nombre'], # se especifica los datos 
        #que se quieren mostrar de ese indice
        "producto": orden['detalles']['producto'],
        }

        print("Segunda orden:")
        print(f"datos obtenidos : {orden}")
         # los imprime despyes de especificar que se quiere ver

clientes_premium = []  

for orden in ordenes_compra:
    
    es_vip = orden['cliente']['es_vip']
    total_pagado = orden['detalles']['total_pagado']
    
  
    if es_vip and total_pagado > 1000:
        nombre = orden['cliente']['nombre']
        clientes_premium.append(nombre)


print("Clientes Premium:")
print(clientes_premium)
print()






reporte_final = []  

for orden in ordenes_compra:
    
    if orden['estado_envio'] == "entregado":
        
        nuevo_registro = {
            "Comprador": orden['cliente']['nombre'],
            "Articulo": orden['detalles']['producto'],
            "Gasto": orden['detalles']['total_pagado']
        }
        
        # 3. Agregar a lista final
        )
        reporte_final.append([orden_compra, clientes_premium, nuevo_registro])

# 4. Exportar archivo JSON
with open('entregas_completadas.json', 'w', encoding='utf-8') as archivo:
    json.dump(reporte_final, archivo, indent=4)

print("Reporte generado correctamente")
print(f"Total entregas completadas: {len(reporte_final)}")