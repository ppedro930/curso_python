import json

#  Abrir y cargar el archivo ventas.json
with open('ventas.json', 'r', encoding='utf-8') as archivo:
    ordenes_compra = json.load(archivo)

#  Imprimir cuántas órdenes existen
print(f"Total de órdenes de compra: {len(ordenes_compra)}\n")



#  NIVEL 2: EXPLORACIÓN (NAVEGACIÓN ANIDADA)


#  Acceder a la segunda orden (índice 1)
segunda_orden = ordenes_compra[1]

# 2. Imprimir nombre del cliente y producto comprado
nombre_cliente = segunda_orden['cliente']['nombre']
producto = segunda_orden['detalles']['producto']

print("Segunda orden:")
print(f"Cliente: {nombre_cliente}")
print(f"Producto: {producto}\n")



# 💎 NIVEL 3: FILTRADO (LÓGICA Y CONDICIONALES)


# 1. Crear lista vacía
clientes_premium = []

# 2. Recorrer todas las órdenes
for orden in ordenes_compra:
    
    # Extraer datos necesarios
    es_vip = orden['cliente']['es_vip']
    total_pagado = orden['detalles']['total_pagado']
    
    # 3. Verificar ambas condiciones
    if es_vip == True and total_pagado > 1000:
        clientes_premium.append(orden['cliente']['nombre'])

# 4. Imprimir lista final
print("Clientes Premium:")
print(clientes_premium)
print()



# ⚙ NIVEL 4: TRANSFORMACIÓN Y CARGA (TRANSFORM & LOAD)


# 1. Crear nueva lista vacía
reporte_final = []

# 2. Iterar nuevamente sobre los datos
for orden in ordenes_compra:
    
    if orden['estado_envio'] == "entregado":
        
        # 3. Crear diccionario simplificado
        registro = {
            "Comprador": orden['cliente']['nombre'],
            "Articulo": orden['detalles']['producto'],
            "Gasto": orden['detalles']['total_pagado']
        }
        
        reporte_final.append(registro)

# 4. Exportar a nuevo archivo JSON con indent=4
with open('entregas_completadas.json', 'w', encoding='utf-8') as archivo_salida:
    json.dump(reporte_final, archivo_salida, indent=4, ensure_ascii=False)

print("Archivo 'entregas_completadas.json' generado correctamente ✅")