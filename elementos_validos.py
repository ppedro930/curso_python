precios = ["100", "200", "no hay precio", "400"]
           
for p in precios:
    try:
        precio_float = float(p) * 1.16
        print(f"Precio convertido: {precio_float:.2f}")
    except ValueError:
        print(f"Error: el valor '{p}' no es un numero valido.")