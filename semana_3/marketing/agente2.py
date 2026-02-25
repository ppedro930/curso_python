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
    



def generar_respuesta(comentario, sentimiento, sugerencia, temperatura):

    print(f"\n--- 1. Generando ideas para: {comentario} sentimiento: {sentimiento} sugerencia: {sugerencia}(Temp: {temperatura}) ---")

    prompt = f"""
    Comentario del cliente: {comentario}

    El sentimiento detectado es: {sentimiento}

    Si es NEGATIVO:
    Redacta una disculpa empática y ofrece contactar al cliente.

    Si es POSITIVO:
    Agradece la preferencia y pide que vuelva pronto.

    Respuesta breve:
    """


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


        
    #funcion que genere prompt para pegarlo en ia y que ese genere la imagen del comentario














    
























































