# # mi_lista =[10,20,30]

# # #print(type(mi_lista).__name__)
# # #print(f"mi lista original{mi_lista}")

# # mi_lista.append(40) #agregar valores

# # print(f"despues de append {mi_lista}")

# # mi_lista.insert(1,50) # inserta un valor en un indice especifico (indice, valor)

# # # print(f"despues de append insert {mi_lista}")

# # nueva_lista= ['a','b','c','d',20,'gdgdg']

# # # lista_unida = []

# # # lista_unida.extend(mi_lista)

# # mi_lista.extend(nueva_lista)

# # # print(lista_unida)

# # #lista extendida
# # # mi_lista.extend(nueva_lista)

# # # print(mi_lista)

# # #eliminar elementos

# # # mi_lista.remove(20) #elimina el primer elemento que encuentra en este caso el 20

# # # print(f"lista despues de eliminar elemento {mi_lista}")


# # # ultimo_elemento = mi_lista.pop()

# # # print(f"tras pop() se elimino el {ultimo_elemento} en la lista y esta es {mi_lista}")

# # # del mi_lista[4]

# # # print(f"lista despues del {mi_lista}")

# # # mi_lista.extend([15,70,15,30,15])
# # # print(f"lista actual {mi_lista}")


# # # valor_find = 'a'
# # # cantidad=mi_lista.count(valor_find)

# # # print(f"el valor a buscar es {valor_find} y aparece {cantidad} veces")
# # valor_index ='a'
# # indice = mi_lista.index('a')
# # # print(f"el valor {valor_index} tiene el indice {indice}")

# # number_list= [50,20,80,10,87,5,3] # para el sort solo funciona con un solo tipo de datos 
# #ejplo si pones letras son solo funciona con letras o numeros... solo funciona con numeros

# # number_list.sort() #solo funciona para numeros
# # print(f"tras sort, se queda como: {number_list}")

# # number_list.sort(reverse=True)

# # # print(f"tras ordenar descendente {number_list}")

# # mi_lista.reverse() # solo voltea la lista al reves no ordena
# # # print(f"tras reverse{mi_lista}")

# # lista_copia =mi_lista.copy()

# # mi_lista.clear()

# # # print(f"la lista original es {mi_lista}")

# # # print(f"la copia de la lista es {lista_copia}")

# # mi_lista= ['manzana','pera','uva']

# # elemento_borrar = 'naranja'

# # try:
# #     mi_lista.remove(elemento_borrar)
# #     print(f"el elemento {elemento_borrar} fue eliminado con exito")
# # except ValueError as e:
# #     print(f"el elemento {elemento_borrar} no se elimino porque no existe en {mi_lista}")

# # indice=10

# # try:

# #     valor = mi_lista[indice]
# #     print(f"el valor en el indice{indice} es {valor}")

# # except IndexError as e:
# #     print(f"el error es porque el indice {indice} no esta en lista")

# #     print(f"\n la lista solo tiene {len(mi_lista)} elementos")
# # try:
# #     lista_vacia = []

# #     elemento_eliminado = lista_vacia.pop()
# #     print(f"valor eliminado es {elemento_eliminado}")
# # except IndexError as e:
# #     print(f"no se puede usar pop en {mi_lista}")
# #     print(f"el mensaje de error es {e}")

# # letras = ["a","b","c","d","e","f","g"]
# # letras = [1,2,3,4,5,6,7,19.4]

# # print(letras[0:3]) # las primeras 3
# # print(letras[2:]) # despues del 2
# # print(letras[:4]) #los primeros 4
# # print(letras[::2]) # de 2 en 2
# # print(letras[::-1]) #de la ultima a la primera

# # if 7 in letras:
# #     print(f"el 7  esta en la lista")
# # else:
# #     print(f"el 7 no esta en la lista")

# # print(f"tamaño {len(letras)}") #calcula elementos de la lista

# # print(f"suma total {sum(letras)}")

# # print(f"mayor {max(letras)}")

# # print(f"menor {min(letras)}")

# # datos = ["juan","perez", 25, "mexico","programador" ]

# # nombre,apellido,*resto_De_datos = datos

# # print(nombre)
# # print(apellido)
# # print(resto_De_datos)

# numeros = [1,2,3,4,5,6,7,8,9,10]

# cuadrados = []

# for n in numeros:
#     cuadrados.append(n*n) # complejidad algoritmica
# print(cuadrados)

# cuadrados_list = [n * n for n in numeros]

# print(cuadrados)

# ########################################

# pares_al_cuadrado = [n*n for n in numeros if n % 2 ==0]

# print(pares_al_cuadrado)

# ###################################################################

mochila = ["pocion", "mapa","cuerda"]

print(f"bienvenido, el contenido inicial de la mochila es {mochila}")

mochila.append('espada')

print(mochila)

mochila.insert(0,"antorcha")

print(mochila)

mochila.remove("cuerda")

print(mochila)


mochila.sort(reverse=False)

print(f"tras ordenar por orden alfabetico {mochila}")


############################################################


elemento_borrar = 'llave dorada'

try:
     mochila.remove(elemento_borrar)

     print(f"el elemento {elemento_borrar} fue eliminado con exito")
except ValueError as e:
     print(f"el elemento {elemento_borrar} no se elimino porque no existe en la lista {mochila}")


######################################

tesoro = ["100_monedas", "rubi", "casco", "botas","guantes"]



dinero,joya,*equipo = tesoro

print(dinero)
print(joya)
print(equipo)

primeros_dos =["100_monedas", "rubi", "casco", "botas","guantes"]

print(primeros_dos[0:2])

############################################################################

oferta_mercader = [15, 80, 5, 120, 25, 90]


oferta = [n *1.5 for n in oferta_mercader if n > 50]
print(oferta)









