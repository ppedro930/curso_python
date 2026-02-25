import os
import time
from dotenv import load_dotenv
from google import genai 
from google.genai import types

load_dotenv()

API_KEY =os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("error: no se encontro el api key.")

try:
    client = genai.Client(api_key=API_KEY)
    print("cliente conectado y listo.")
except Exception as e:
    print(f"error al conectar el cliente: {e}")
    exit() #sirve para terminan el programa de python 

def analizar_sentimiento(texto_usuario):
    
    promt_sistema = """

    eresn un analista de datos senior.
    clasifica el siguiente texto en positivo, negativo o neutro:
    responde solo en mayuscula con la egtqueta correspondiente, sin markdown ni explicaciones.

    """

    texto_completo = f"{promt_sistema}\n\ntexto a evaluar: {texto_usuario}"
    #configuracionnnnnnnnnnnnnnn parametrossssssssssssssss apuntarrrrrrrrrrrrr

    confguracion = types.GenerateContentConfig(
        temperature=0.0,
        top_k=20,
        top_p=0.95,
        candidate_count=1

    )

    '''
A. Temoerature (creatividad)

Este parametro controla, lo  alocada o creativa que es la IA.

si el valor es 0,la IA se vuelve determinista, es decir que siempre se escogera la palabra mas probable.
ideal para clasificacion de datos.

Usualmente, el rango es de 0 a 2, por lo que si el valor es 1 o 2, la IA toma riesgos, 
es decir se vuelve mas creativa al elegir palabras no tan probables.

Este codigo en particular usa el valor de 0 para clasificar el texto en POSITIVO NEGATIVO o NEUTRO.

**********************************************************************************************

TOP_k = 20

imaina que la IA tiene el diccionario con 100.000 palabraas (por decir un munero) posibles para
responder.

sin el argumento "top_k", la IA podria escoger cualquier palabra, incluso una palabra que casi nadie usa.

con el argumento "top_k=20", la IA solo puede escoger entre las 20 palabras mas probables,
 lo que hace que las respuestas sean mas coherentes y relevantes.
***********************************************************************************************

top_p (calidad o zona segura)

en el sentido mamtematico es decirle a la IA lo siguiente:

de todas las palabras que encontraste, ve sumando las probabilidades desde las mas alta hasta llegar al 95%

como analogia, es como decirle al vigilante que deje pasar solo a las personas que tengan alta probabilidad de 
consumir.

ejplo

Persona A =90% 
Persona B = 1%
Persona C = 4%

el vigilante al saber estas probabilodades e indicarle que las sume hasta llegar al 95% 
dejaria pasar a la persona A,B y C, pues juntos sumaran el 95% por lo tanton segun la IA podrian
consumir en el antro.

Analogia 2:

supon, que tienes la siguiente frase: "el gato esta..."

- Si top_p=1.0 (100%), la IA alucina entonces podria contestar algo como:

"... bailand salsa en la luna"

- si top_p=0.95 (95%), la IA se vuelve mas normal o destructiva, entonces la respuesta seria como:
"... durmiendo en el sofa"

- si top_p=0.5 (50%), la IA se vuelve mas enfocada, por lo que su respuesta podria ser:
"... durmiendo"

si top_p=0.1 (10%), la IA usa la palabra mas cora posible  como:

"...en"

    | Valor top_p | %    | Analogía            | ¿Cómo actúa la IA?                               | ¿Para qué sirve?                              |
    | ----------- | ---- | ------------------- | ------------------------------------------------ | --------------------------------------------- |
    | 1.0         | 100% | La Fiesta Loca      | Creativa, arriesgada, a veces alucina.           | Poemas, lluvia de ideas, chistes.             |
    | 0.95        | 95%  | El Antro de Moda    | Equilibrada. Inteligente pero con sentido común. | Chatbots generales (Tu caso).                 |
    | 0.5         | 50%  | La Junta de Oficina | Correcta, formal, va al grano.                   | Manuales, noticias, resúmenes serios.         |
    | 0.1         | 10%  | El Robot Aburrido   | Repetitiva, monótona, vocabulario pobre.         | Tareas muy mecánicas o matemáticas estrictas. |

*************************************************************************************************************

candidate_count = 1.

este argumento le indica a la IA la cantidad de respuestas a considerar.
en nuestrpo caso solo queremos que nos responda una vez si se quisiera que responda 5 veces entonces

candidate_count=5

nota, no necesariamente nos dara 5 respuestas mas bien tendra 5 versiones para responder y lo hara 
con la mejor de acuerdo a sus probabilidades analizadas.

'''
    print(f"\n analizando el el texto... {texto_usuario}")
    inicio = time.time()
    try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", # gemini-flash-latest, gemini-2.5-flash
                contents=[types.Part.from_text(text=texto_completo)],
                config=confguracion
        )
        
            t_in = response.usage_metadata.promt_token_count if response.usage_metadata else 0
            t_out = response.usage_metadata.candidates_token_countt if response.usage_metadata else 0

            fin = time.time()
            duracion = round(fin-inicio, 2)

            return response.text.strip(), duracion, t_in, t_out

    except Exception as e:  
            return f"error api: {str(e)}", 0, 0, 0
    
if __name__ == '__main__':
    textos = [
         "el gato es muy viejo y travieso",
         "mi compañero de clase es bien atento",
         "mi archivo pesa 2gb"
                ]    
    
    print("\n --- iniciando proceso de analisis  ---\n")

    for t in textos:
        resultado, tiempo, tokens_soluicitud, tokens_respuesta = analizar_sentimiento(t)

        if "ERROR" in resultado:
            print(f"el error es: {resultado}")
        else:
            print(f"sentimiento: {resultado}")
            print(f"tiempo de respuesta: {tiempo} segundos")
            print(f"tokens usados en la solicitud: {tokens_soluicitud} in + {tokens_respuesta} out = {tokens_respuesta + tokens_soluicitud} total")
            print("**"*25)

            print(" --- esperando para no sobrepasar los limites  ---")
            time.sleep(4)
        print("\n --- proceso de analisis finalizado  ---")




