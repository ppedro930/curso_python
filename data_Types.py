# repaso datatypes
'''diferentes tipos de variables en python'''

usuario_raw = '"anGEL rOdriGuez Altamaerina"'  # variable tipo string

id_usuario = 2026 # -> variable tipo integer
ventas_realizadas = 15  # -> variable tipo 

precio_producto = 450.757474  # -> variable tipo float
tasa_iva = 0.18  # -> variable tipo float

nombre_producto = "Memoria USB 64 GB"  # -> variable tipo string
categoria = "Accesorios"  # -> variable tipo string

tiene_descuento = True  # -> variable tipo boolean
es_importado = False  # -> variable tipo boolean
comentario_cliente = None  # -> variable tipo NoneType

precios_semanales = [450.75, 440.0, 460.50, 450.75]  # -> variable tipo list
margen_seguridad = (100.0, 1000.0 )  # -> variable tipo tuple
categorias_unicas = {"Accesorios", "Hardware", "Accesorios"}  # -> variable tipo set

registro_ventas = {
    "id": id_usuario,
    "producto": nombre_producto,
    "aplico_descuento": tiene_descuento,
    "comentario": comentario_cliente,
    "precio_semanal": precios_semanales
  }  # -> variable tipo dictionary

# print(f"Analizando comentario del producto: {registro_ventas['precio_semanal']}")

if registro_ventas["comentario"] is None:
    print("Alerta: el registro no tiene comentarios del cliente.")
total = precio_producto * (1 + tasa_iva)
# print(f"El total con IVA es: {total} ({total:.2f})")

producto_1 = {
    "id": 101,
    "nombre": "teclado inalambrico",
    "precio": 850,
    "en oferta": False,
    "comentarios": None
}

inventario = [producto_1, # -> diccionario 1
              {"id": 102, "nombre": "mouse", "precio": 450, "en oferta": True, "comentarios": "buen producto"}, # -> diccionario 2
              {"id": 103, "nombre": "monitor", "precio": 3500, "en oferta": False, "comentarios": None} # -> diccionario 3
              ]

total_precios = 0
for p in inventario:
    total_precios += p["precio"]

promedio = total_precios / len(inventario)
print(f"El precio promedio de los productos en el inventario es: {promedio:.2f}, el total de precios es: {total_precios:.2f}")

sin_comentarios = 0
for p in inventario:
    if p["comentarios"] is None:
        sin_comentarios += 1

print(f"Analisis terminado: \n- productos por revisar (sin comentarios) {sin_comentarios}")
print(f"precio promedio: ${promedio:.2f} \n- precio tottal: ${total_precios:.2f}")

