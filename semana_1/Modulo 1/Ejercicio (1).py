libreria = {
    "nombre": "Lectura Infinita",
    "sucursales": ["Centro", "Norte", "Online"],
    "catalogo": [
        {
            "id": "LIB001",
            "titulo": "El Quijote",
            "detalles": {"autor": "Cervantes", "paginas": 863},
            "precios": [15.0, 12.5, 10.0]  # Tapa dura, blanda, digital
        },
        {
            "id": "LIB002",
            "titulo": "Cien años de soledad",
            "detalles": {"autor": "García Márquez", "paginas": 471},
            "precios": [20.0, 18.0] # Tapa dura, blanda
        },
        {
            "id": "LIB003",
            "titulo": "1984",
            "detalles": {"autor": "George Orwell"}, # Falta 'paginas'
            "precios": [12.0, 9.5, 7.0]
        }
    ]
}


#1.El Respaldo de Seguridad
#Accede al nombre de la librería utilizando el método .get(). Si por alguna razón la llave 
# "nombre" no existiera, 
#el sistema debe devolver "Librería Genérica".





#nombre_libreria = libreria.get("nombre", "Librería Genérica")
#print(nombre_libreria)






#2. Navegación en Profundidad
#Obtén el autor del segundo libro en el catálogo ("Cien años de soledad").
#  Recuerda que el catálogo es una lista 
#y los detalles son otro diccionario.






#autor_segundo_libro = libreria["catalogo"][1]["detalles"]["autor"]
#print(autor_segundo_libro)




#3. El Precio Digital
#Extrae el precio digital (el tercer elemento de la lista de precios) del primer libro ("El Quijote"). 
#Guarda este valor en una variable llamada precio_final.






#precio_final = libreria["catalogo"][0]["precios"][2]
#print(precio_final)




#4. Manejo de Datos Faltantes
#Intenta obtener el número de páginas del tercer libro ("1984") usando .get(). 
#Como este dato no existe en el diccionario de ese libro, haz que el método devuelva 
# el mensaje "Información no disponible".



#paginas_1984 = libreria["catalogo"][2]["detalles"].get(
 #   "paginas", 
  #  "Información no disponible"
#)

#print(paginas_1984)




#5. Acceso a Sucursales
#Accede a la lista de sucursales y obtén específicamente la última de la lista 
# ("Online") usando un índice negativo.




ultima_sucursal = libreria["sucursales"][-1]
print(ultima_sucursal)



L = [1, 2, 3, 4, 5]
# acceder a 1 en negativo

print(L[:-1])  # Salida: 1

print(L[4:])  # Salida: 1

# :n -> desde el inicio hasta n-1 (se imprime hasta el elemento n)
# n: -> desde n hasta el final (se imprime desde el elemento n)

#acceder a 5 
