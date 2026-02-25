producto = {
    "sku": "AC12345",
    "nombre": "Audífonos Bluetooth",
    "stock" : 150,
    "precio": 1200.50,
}

busqueda ="descuento"
#valor = producto[busqueda]
valor_get = producto.get(busqueda)
valor_get = producto.get(busqueda, 0)
#valor_get = producto.get(busqueda, "No disponible")

# print(f"valor usando llave dinamica (keyError): {valor_get}")

ventas_semana =[
    {"dia": "Lunes", "montos": [150.0, 200.5, 300.75]},
    {"dia": "Martes", "montos": [400.0, 700.5, 500.75]},
    {"dia": "Miercoles", "montos": [300.0, 100.5, 400.75]}
]

indice_dia = 0  # Lunes
indice_monto = 2
venta_1_lunes = ventas_semana[0]["montos"][0]
dia_ventas = ventas_semana[0]["dia"]

print(f"Venta {indice_monto +1} del {dia_ventas}: {venta_1_lunes:.2f}")

total_lunes = sum(ventas_semana[0]["montos"])

ventas_max_martes = max(ventas_semana[1]["montos"])

ventas_totales_por_semana = 0

for dia in ventas_semana:
    ventas_totales_por_semana += sum(dia["montos"]) # -> (+=) ventas_totales + sum(dia["montos"])

    print(f"suma total de ventas en la semana: ${ventas_totales_por_semana:.2f}")