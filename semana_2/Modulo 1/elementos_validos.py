precios = ["100", "200", "no hay precio", "400"]
           
for p in precios:
    try:
        precio_float = float(p) * 1.16 #se convierte y se multiplica por el valor asignado
        print(f"Precio convertido: {precio_float:.2f}") # .2f muestra el numero a 2 decimales
    except ValueError:
        print(f"Error: el valor '{p}' no es un numero valido.")