import json

with open('users.json', 'r', encoding='utf-8') as archivo:
    usuarios = json.load(archivo)

usuarios_limpios = []

for u in usuarios :
    nombre = u['name']
    correo =u['email']
    empresa = u['company']['name']
    ciudad = u['address']['city']

    perfil_marketing = {
        "nombre_completo":nombre,
        "email_contacto":correo,
        "compañia":empresa,
        "ubicacion":ciudad
    }

    usuarios_limpios.append(perfil_marketing)

print("transformacion completada")
print(f"vistazo al primer registro limpio \n{usuarios_limpios}\n")

with open('marketing_leads.json', 'w', encoding='utf-8') as archivo_nuevo:
    json.dump(usuarios_limpios, archivo_nuevo, indent=2)

print("exito... los datos han sido cargados en 'marketing_leads.json'.")

print("revisa la carpeta el nuevo archivo te espera")
print("\n=== pipeline etl finalizado ===")