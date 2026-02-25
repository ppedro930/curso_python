import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("¡Error! No se encontró la API KEY en el archivo .env")

client = genai.Client(api_key=API_KEY)

total_inputs_tokens = 0
total_outputs_tokens = 0


def auditoria_costos(input_t, output_t, paso):

    global total_inputs_tokens, total_outputs_tokens

    if input_t is None: input_t = 0
    if output_t is None: output_t = 0

    total_inputs_tokens += input_t
    total_outputs_tokens += output_t

    print(f"[Auditoria {paso}] Tokens Entrada: {input_t} | Tokens Salida: {output_t}")

def generar_texto(modelo, prompt, configuracion):

    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:

        try: 

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=configuracion
            )

            return response
        
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or 'quota' in error_str.lower():
                print(f"\nAlerta, Google pidio esperar. (Intento {intentos+1}({max_intentos}))")
                print("Durmiendo 30 segundos para intentar de nuevo")
                time.sleep(30)
                intentos += 1
            else:
                raise e

    raise Exception ("Se agotaron los intentos, la API sigue ocupada") 


def generar_slogan(producto,temperatura):

    print(f"\n--- 1. Generando ideas para: {producto} (Temo: {temperatura}) ---")

    prompt = f"""Genera 3 slogans cortos, impactantes y modernos para este producto {producto}"""

    response = generar_texto(
        modelo='gemini-2.5-flash-lite',
        prompt=prompt,
        configuracion=types.GenerateContentConfig(
            temperature=temperatura, 
            top_k = 40, 
            system_instruction='Eres un director Creativo experto. Tus respuestas son breves'
        )
    )

    t_in = response.usage_metadata.prompt_token_count
    t_out = response.usage_metadata.candidates_token_count

    auditoria_costos(t_in, t_out, 'Creatividad')

    return response.text

def analizar_impacto(slogan):
    print(f"\n--- 2. Analizando impacto del slogan... ---")

    indicaciones = f""" 
    Analiza el siguiente slogan y dime si el sentimiento es:
    ATRACTVO, AGRESIVO o ABUSIVO. 
    Responde solo con una palabra: '{slogan}'
    """

    response = generar_texto(
        modelo='gemini-2.5-flash-lite',
        prompt=indicaciones,
        configuracion=types.GenerateContentConfig(
            temperature=0.0,  
            system_instruction='Eres el jefe de un director Creativo experto. Por ello tu respuesta es objetiva'
        )
    )

    t_in = response.usage_metadata.prompt_token_count
    t_out = response.usage_metadata.candidates_token_count

    auditoria_costos(t_in, t_out, 'Analisis')

    return response.text.strip()


def generar_prompt_imagen(descripcion_visual):

    print(f"\n--- 3. Diseñando prompt para generar una imagen del producto ---")

    prompt_tecnico = f"""

    Tu tarea es tomar esta simple del usuario: "{descripcion_visual}"

    Y convertirla en un PROMPT altamente detallado y artistico en IGNLÉS
    Debes incluir explicitamente: 

    1.- Sujeto principal (detallado).
    2.- Estilo artistico (Acuarea, render, etc)
    3.- Iluminacion (Neon, soft, shadows, etc)
    4.- Camara y render (8k, octane render, wide angle)

    Salida esperada: Solo entrega el texto dle prompt en inglés sin explicaciones adicionales
    """
    response = generar_texto(
        modelo='gemini-2.5-flash-lite',
        prompt=prompt_tecnico,
        configuracion=types.GenerateContentConfig(
            temperature=0.8,  
            system_instruction='Actua como un experto en prompt Enginering paa Midjourney, dall-E y Stable difusion'
        )
    )

    t_in = response.usage_metadata.prompt_token_count
    t_out = response.usage_metadata.candidates_token_count

    auditoria_costos(t_in, t_out, 'Prompt Engineering')

    return response.text.strip()


if __name__ == "__main__":

    try:

        producto_usuario = input("Ingresa el nombre de tu producto (ej. Tenis voladores)")

        ideas = generar_slogan(producto_usuario, temperatura=0.9)
        print(f"\nResultados de slogans: \n {ideas}")

        mejor_slogan = input("\n Copia y pega aqui tu slogan favorito:  ")
        impacto = analizar_impacto(mejor_slogan)
        print(f"\n La IA dice que el impacto del slogan es **{impacto}**")

        print("\n Ahora se dieñará la imagen del producto")
        desc_visual = input("Dame una idea base (ej. Zapatos neon en el espacio): ")

        imagen = generar_prompt_imagen(desc_visual)

        print("\n" + "#"*60)
        print(" copia y pega este pompt en tu generador de imagenes favorito")
        print("#"*60)
        print(f"\n{imagen}\n")
        print("#"*60)

        print("\n" + "$"*80)
        print("REPORTE FINANCIERO")
        print("$"*80)
        print(f"Producto: {producto_usuario}")
        print(f"Total Tokens Entrada: {total_inputs_tokens}")
        print(f"Total Tokens Salida: {total_outputs_tokens}")
        
        costo = ((total_inputs_tokens + total_outputs_tokens) / 1_000_000) * 0.10
        print(f"Costo aroximado de esta ejecución: ${costo:.8f} USD")
        
    except Exception as e:
        print(f"\n🛑 Error crítico en el programa: {e}")
        
    #funcion que genere prompt para pegarlo en ia y que ese genere la imagen del producto