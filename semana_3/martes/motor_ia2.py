import time
from google.genai import types
from config import client

#en motor ia añadir funcion que convierte a imagen bin y cloud y mandar a llamar ia_test_or objetivo=convertir a binario y otro metodo











def analizar_sentimiento(texto_usuario):
    
    instruccion_sistema = (
        "Eres un analista de datos experto. "
        "Clasifica el texto en: positivo, negativo o neutral. "
        "Responde solo con la etiqueta, sin markdown ni explicaciones."
    )

    configuracion = types.GenerateContentConfig(
        system_instruction=instruccion_sistema,
        temperature=0.0,
        top_p=0.95,
        top_k=20,
        candidate_count=1
    )

    inicio = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[texto_usuario],
            config=configuracion
        )

        nombre_real_modelo = getattr(response, "model_version", "desconocido")

        t_in = getattr(response.usage_metadata, "prompt_token_count", 0) if response.usage_metadata else 0
        t_out = getattr(response.usage_metadata, "candidates_token_count", 0) if response.usage_metadata else 0

        duracion = round(time.time() - inicio, 2)

        return response.text.strip(), duracion, t_in, t_out, nombre_real_modelo

    except Exception as e:
        return f"Error api: {str(e)}", 0, 0, 0, 0































def analizar_imagen_bin(img_bytes):
    
    instruccion_sistema = (
        "Actua como un zoologo experto"
        "Identifica al animal que aparece en la imagen"
        "Solo dame el nombre sin explicaciones ni markdown"
    )

    configuracion = types.GenerateContentConfig(
        system_instruction=instruccion_sistema,
        temperature=0.0,
        top_p=0.95,
        top_k=20,
        candidate_count=1
    )

    inicio = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Part.from_text(text=instruccion_sistema),types.Part.from_bytes(
                    data=img_bytes,
                    mime_type="image/png")],
            config=configuracion
        )

        nombre_real_modelo = getattr(response, "model_version", "desconocido")

        t_in = getattr(response.usage_metadata, "prompt_token_count", 0) if response.usage_metadata else 0
        t_out = getattr(response.usage_metadata, "candidates_token_count", 0) if response.usage_metadata else 0

        duracion = round(time.time() - inicio, 2)

        return response.text.strip(), duracion, t_in, t_out, nombre_real_modelo

    except Exception as e:
        return f"Error api: {str(e)}", 0, 0, 0,0

""" 
with open("actividad.jpg", "rb") as f:
    imagen_bytes = f.read() """


# LLAMAR FUNCION

""" texto = analizar_imagen_bin(imagen_bytes)

print("\nRespuesta del modelo:")
time.sleep(4)
print(texto)

 """
















def analizar_imagen_cloud(path_imagen):

    instruccion = "que animal es el que se ve en esa imagen nada mas el nombre"

    inicio = time.time()

    try:

        archivo = client.files.upload(file=path_imagen)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                instruccion,
                types.Part.from_uri(
                    file_uri=archivo.uri,
                    mime_type=archivo.mime_type
                )
            ]
        )

        duracion = round(time.time() - inicio, 2)

        return (
            response.text.strip(),
            duracion,
            getattr(response.usage_metadata, "prompt_token_count", 0),
            getattr(response.usage_metadata, "candidates_token_count", 0),
            getattr(response, "model_version", "desconocido")
        )

    except Exception as e:
        return f"Error api: {str(e)}", 0, 0, 0, "error"
