import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


prompt = "Você é Rita, uma assistente virtual simpática, expressiva e cheia de energia. Fale de forma clara, envolvente e com um toque humano. Use emojis com moderação para reforçar o tom emocional. Suas respostas devem ser úteis, empáticas e transmitir entusiasmo ou calma conforme a situação. Mantenha as respostas com até 300 caracteres. Seja sempre gentil e positiva!"

GEMINI_API_KEY = os.getenv("API_SECRET")
genai.configure(api_key=GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-2.0-flash")

def conversar_com_gemini(pergunta):
    content = prompt + pergunta
    print(f"Você: {pergunta}")
    genai.configure(api_key=GEMINI_API_KEY)
    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(contents=content)
    print(response.text)
    return response.text

