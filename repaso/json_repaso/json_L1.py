import json

texto_json='''

{
"nombre": "arthur",
"clase": "guerrero",
"nivel": 5,
"es_vip": true,
"mascota": null

}

'''

print(f"tipo de dato de texto_json: {type(texto_json)}") # aca lo reconoce cmo texto

perfil_python = json.loads(texto_json) # aca se convierte a json
print(f"tipo de dato {type(perfil_python)}")
print(f"nombre jugador: {perfil_python["nombre"]}")
print(f"es vip? {perfil_python["es_vip"]}")

perfil_python["nivel"] =6
perfil_python["oro"] =150
perfil_python["es_vip"] =False

print(f"perfil actualizado en python: {perfil_python}")
print("-"*50)

nuevo_texto_json = json.dumps(perfil_python, indent=2)

print("asi se ve el texto json para exportar")
print(nuevo_texto_json)
print(f"tipo de dato de salida {type(nuevo_texto_json)}")



