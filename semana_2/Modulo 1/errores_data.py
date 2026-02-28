try:
    edad = "25"
    # edad = int(edad)
    proximo = edad + 1
    print(proximo)
except TypeError as error:
    print(f"Error de suma: No se puede sumar un string con un int. Python no sabe si quieres 25 o '25'")
    print(f"Detalle del error: {error}")