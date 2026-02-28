alumno = {"nombre":"ana", "edad":25, "curso":"python"}

# print(f"diccionario base {alumno}")
# print(f"acceso directo valido ['nombre'] -> {alumno['nombre']}")

# try:
#     print(alumno["calificacion"])
# except KeyError as e:
#     print(f" error (keyerror) {e}")
#     print("explicacion si usas corchetes y la clave no existe el programa explota")

# print(f"usando .get('calificacion): {alumno.get('calificacion')}")
# print(f"usando .get con valor por defecto {alumno.get('calificacion', 'no existe el campo')}")

#print(f"para que funcione hash debe ser inmutable{hash('nombre')}")

diccionario_valido = {(1,2): "coordenadas"} #si (1,2) se pone asi [1,2] no funciona las listas mutan
# las tuplas no... 

inventario = {"manzanas":10, "peras":5,"naranjas":20} #se puede iterar

# for item in inventario:
#     print(item)

# for clave,valor in inventario.items():
#     print(f"hay {valor} {clave}")

# del inventario["peras"]
# print(inventario)

# eliminado = inventario.pop("uvas", "no habia uvas para borrar")
# print(f"resultado de pop(úvas): {eliminado}")

# peras_borrar =inventario.pop("peras")
# print(f"borra peras({peras_borrar}). nuevo inventario {inventario}")

dict_1 ={"a":1, "b":2}
dict_2 ={"b":99,"c":3}

dict_1.update(dict_2)
dict_1.update({'nombre':'angel','edad':40})
dict_1.update({'puesto':'inge'})
#print(dict_1)

dict_fusionado = dict_1 | dict_2
#print(f"fusion con operador '|' {dict_fusionado}")

numeros =[1,2,3,4,5]
cuadrados={n: n**2 for n in numeros if n % 2 != 0 }
#print(f"diccionario de cuadrados (solo impares): {cuadrados}")

perfil = {
    "nombre": "arthur",
    "clase": "guerrero",
    "nivel": 5,
    "oro": 150
}

print(perfil)

perfil["edad"] = 25 #agregar campos y registros
perfil["nivel"] =6 # o modificar
perfil["oro"] = perfil["oro"] - 50

#print("\n --- fase 1: perfil actualizado---")

#print(perfil)

#print("\n llaves del dicc cols en pandas")

#print(perfil.keys())

misiones = [
    {"id":1, "titulo":"cazar slimes", "recompensas_oro":50, "nivel_minimo":2},
    {"id":2, "titulo":"escoltar mercader", "recompensas_oro":120, "nivel_minimo":5},
    {"id":3, "titulo":"derrotar al dragon", "recompensas_oro":5000, "nivel_minimo":20}
]


mision_extraida = misiones[1]['titulo']
print(f"la segunda mision {mision_extraida}")
      
def evaluar_misiones(jugador, lista_misiones):
    print(f"\n revisando tablon paar {jugador['nombre']} (nivel {jugador['nivel']})...")    

    for mision in lista_misiones:
        if jugador["nivel"] >= mision['nivel_minimo']:
            print(f"aceptada: puedes hacer '{mision['titulo']}' por {mision['recompensas_oro']} de oro")
        elif jugador['nivel'] == mision['nivel_minimo'] -1:
            print(f"casi: te falta solo el nivel 1 para {mision['titulo']} sigue intentando")
        else:
            diferencia = mision["nivel_minimo"] - jugador["nivel"]
            print(f"bloqueada {mision['titulo']} es muy peligrosa te faltan {diferencia}")

evaluar_misiones(perfil,misiones)


def simular_combate(nombre_jugador, hp_enemigo):

    print(f"\n {nombre_jugador} ha encontrado un mosntruo con {hp_enemigo}")

    ronda=1
    danio_por_golpe= 15

    while hp_enemigo > 0:
        print(f"ronda {ronda}: atacas causando {danio_por_golpe} de daño")
        hp_enemigo -= danio_por_golpe

        if hp_enemigo < 0:
            hp_enemigo = 0
        print(f"     -> hp del monstruo restante {hp_enemigo}")
        ronda += 1
    print(f"victoria el monstruo ha sido derrotado en {ronda - 1} rondas")
    
simular_combate(perfil["nombre"], 50)

print("---------------------------------------------------------------------------------")

heroe = {
    "nombre": "arthur",
    "hp": 100,
    "pociones":2,
    "danio base": 25
}

dragon = {
    "nombre": "dragon de los datos nulos",
    "hp": 120,
    "danio base": 15
}

print(f"un {dragon['nombre'].upper()} salvaje aparece \n")
