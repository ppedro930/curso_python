import time

# inventario_pociones = ["pocion menor", "pocion mayor","pocion de veneno", "elixir maximo"]

# #objeto iterable

# # for pocion in inventario_pociones:
# #     #print(pocion)
# #     if pocion == 'pocion de veneno':
# #         print("cuidado te puedes envenenar si la usas contigo mismo")
    
# #     print("objeto guardado en la mochila")

#     #time.sleep(0.5)
# resistencia_pico = 100
# oro_recolectado = 0
# golpe_energia = 25

# while resistencia_pico > 0:
#     print(f"tu pico tiene resistencia de {resistencia_pico}")
#     oro_recolectado += 15
#     resistencia_pico -= golpe_energia
#     print(f"encontraste 15 oro {oro_recolectado}")
#     time.sleep(0.5)


# clientes_en_fila = ["guerrero", "mago","ladron", "campesino","rey" ]
# horas_de_luz =3

# while horas_de_luz > 0:

#     if clientes_en_fila:
#         clientes_actual = clientes_en_fila.pop(0) # el .pop es para que 
#         #identifique y elimine el registro desde el indice cer en este caso
#         print(f"mercader: sigueme que quieres comprar {clientes_actual}?")
#     else:
#         print("mercader: no hay mas clientes cerrate temprano")
#         break

#     horas_de_luz -= 1
#     time.sleep(1.5)

#     if clientes_en_fila:
#         print("los siguientes clientes se quedaron sin comprar")
#         for rezagado in clientes_en_fila:
#             print(f" - {rezagado} (regresara mañana)")

    
#     if clientes_en_fila:
#         print("los siguientes clientes se quedaron sin comprar")
#         for rezagado in clientes_en_fila:
#             print(f" - {rezagado} (regresara mañana)")





##########################################################


def analisis_ventas():  #para que no de errores de identacion se define una funcion vacia y se 
    #manda a llamar al finalizar para que ejecute
    ventas_crudas = [
        {"id_ticket":"T-001", "producto": "Laptop", "precio_base": 15000, "status":"completado"},
        {"id_ticket":"T-002", "producto": "Mouse", "precio_base": None, "status":"completado"},
        {"id_ticket":"T-003", "producto": "Teclado", "precio_base": 800, "status":"completado"},
        {"id_ticket":"T-004", "producto": "Monitor", "precio_base": -3500, "status":"completado"},
        {"id_ticket":"T-005", "producto": "Cable HDMI", "precio_base": 250, "status":"completado"}
    ]

    ventas_limpias = []
    ingreso_total = 0
    tasa_iva = 0.16

    for venta in ventas_crudas:
        print(f"procesando ticket y venta {venta["id_ticket"]}")

        if venta["status"] == 'cancelado':
            print("ticket cancelado. saltando registro")
            continue
        precio = venta.get('precio_base')
        if precio is None:
            print("error precio faltante asignado 0m por defecto")
            precio= 0
        elif precio < 0:
            print(f"error el precio es negativo {precio} convertir a positivo")
            precio = abs(precio)
        precio_con_iva = precio * (1 + tasa_iva)
        precio_final =round(precio_con_iva,2)

        venta["precio_final"] =precio_final
        ventas_limpias.append(venta)
        ingreso_total += precio_final

        print(f"procesado con exito precio fin {precio_final}")

    print("\n--- resumen del dia  ---")

    print(f"tickets validos procesados: {len(ventas_limpias)}")
    print(f"ingreso total calculado $ {round(ingreso_total, 2)}")
analisis_ventas() #se manda a llamar la funcion otra vez para que ejecute lo que hay en ella
#si no se hace da error de identacion

