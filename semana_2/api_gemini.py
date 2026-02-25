import os
from google import genai

os.environ["GEMINI_API_KEY"] = "AIzaSyCo1BZ56IlNCXYMcSStV0rY8IdAMNjjLE8"

client = genai.Client()

def gemini(prompt_text:str) -> str:

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text
        )
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    prompt = "que parámetros se necesitan para configurar la respuesta de un chatbot o IA generativa"
    respuesta = gemini(prompt)
    print(respuesta)







