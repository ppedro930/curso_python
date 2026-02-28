'''
uso de isinstance y type para el tipo de variables y errores.

tambien se verifico el uso de type().__name__ para obtener el tipo
sin atributo class. es decir, pasar de esto  <class 'float'> a esto float

'''


# numero =92.
# texto = "hola"

# if type(numero) ==int:
#     print(f"es un entero el numero {numero}")

# if isinstance(numero,float): # la funcion isinstance es para preguntar
#         print(f"el numero es entero{type(numero).__name__}")
# else:
#         print("variable no encontrada")

# if type(texto) ==str:
#        print(f"es cadena de texto {texto}")

# if isinstance(texto,str):
#     print(f"la variable '{texto}' es de tipo {type(texto).__name__} ")
# else:
#     print(f"la variable {texto} no es de tipo str")

'''manejo de errores para cadenas cuando se concatenan cadenas coin mumeros
las ultimas lineas muestran la solucion

'''

#mensaje = "tengo" + 25 + "años"

#print(mensaje)

# try:

#     mensaje = "tengo" + 25 + "años"
# except TypeError as e: # handalear errores... es para que el codigo no se detenga y se siga ejecutando
#     print(f"el mensaje de error es {type(e).__name__}")
#     print(f"el mensaje de error es {e}") # esto es para que se ejecute y continue 
   
# ctrl } para comentar


# mensaje = "tengo " + str(25) + " años"

# print(mensaje)

'''representacion de inmutabilidad  de la variabke tipo cadena

'''

# palabra = "python"

# try:


#     palabra[0] ="T"

# except TypeError as e:
#     print(f"error {type(e).__name__}")
#     print(f"error es {e}")

# palabra = "T" + palabra[1:]

# print(palabra)

# ctrl } para comentar


'''
slicing en variables tipo string tambien funciona en tipo lista y tupla

'''

# alfabeto = "abcdefghijklmnopqrstuvwxyz"

# print(f"alfabeto {alfabeto}")

# print(f"alfabeto primeras 5 {alfabeto[:5]}")

# print(f"alfabeto ultimas 3 {alfabeto[-3:]}")

# print(f"alfabeto de la 10 en adelante {alfabeto[10:]}")

# # ###ctrl } para comentar

# """imprimir de la 12 a la 15, solo la ultima... solo la 10 ... de la 15 a 20"""

# print(f"alfabeto 12 a 15 {alfabeto[11:14]}")

# print(f"alfabeto ultima {alfabeto[-1]}")

# print(f"alfabeto solo 10 {alfabeto[9]}")

# print(f"alfabeto 15 a 20 {alfabeto[14:20]}")

# print(f"invertir cadena solo con slices([::-1]): {alfabeto[::-1]}")

# print(f"saltos de 4 en 4 ([::4]): {alfabeto[::4]}")

'''
memoria de strings cuando es string o tupla los almacena igual pero 
cuando son lista ya los almacena independiente
'''

a= ("hola_mundo")

# b=("hola_mundo")

# print(f"tienen el mismo contenido? a==b -> {a == b}")

# print(f"son el mismo objeto en memoria? a is b -> {a is b}")
# print(f"id de a: {id(a)} | id de b: {id(b)}")


'''metodos de concatenacion o union de strings'''

palabras = ["Python", "es","un", "lenguaje", "increible"]

resultado = ""

''' metodo de concatenacion'''

# for ch in palabras:
#     resultado = resultado + ch + "-"
#     #resultado += ch + "-"

# print(resultado)

'''metodo 2'''

# resultado= "-".join(palabras)
# print(resultado)

''' formateador f-string'''

nombre = "pedro"
pi = 3.14159265

# print("hola {} el valor de pi es {:.2f}".format(nombre,pi)) # -> version antigua
# print(f"hola {nombre} el valor de pi es {pi:.2f}")

# con_nombre_de_variable = 100 * 1.16

# print(f"valor del precio con iva {con_nombre_de_variable:.2f}") #sale sin nombre variable
# print(f"valor del precio con iva {con_nombre_de_variable=:.2f}") #sale con nombre variable

# texto_sucio = "    \n\t hola mundo \n   "
# print(f"texto original eliminando espacios {texto_sucio.strip()}")

# datos_csv = "manzana,pera,platano"
# print(f"lista generagada {datos_csv.split(',')}")

