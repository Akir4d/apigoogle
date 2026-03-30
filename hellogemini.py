import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

# Configura API Key da variabile d'ambiente
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.2,      # 0=deterministico, 1=creativo
    "max_output_tokens": 1024,
    "top_p": 0.8,
}

safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}


model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="""
    Sei un esperto Cyber Security Analyst.
    Analizza i dati forniti e rispondi in modo tecnico ma comprensibile.
    Se non sei sicuro, dillo esplicitamente.
    """
)

# Genera rispostaSpiega cos'è un attacco SQL Injection in 3 righe
response = model.generate_content("Spiega cos'è un attacco SQL Injection in 3 righe")

# Stampa output
print(response.text)