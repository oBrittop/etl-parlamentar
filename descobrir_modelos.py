import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()
CHAVE_IA = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_IA)

print("🔍 Buscando modelos disponíveis na sua conta do Google...\n")

# Lista todos os modelos que suportam geração de conteúdo
for modelo in genai.list_models():
    if 'generateContent' in modelo.supported_generation_methods:
        print(f"Nome exato para usar no código: {modelo.name}")

print("\n✅ Busca concluída!")