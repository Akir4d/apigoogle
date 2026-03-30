import os
from google import genai

# Configurazione della chiave API
CHIAVE_API = os.environ.get("GEMINI_API_KEY", "LA_TUA_CHIAVE_QUI")

# Inizializzazione del Client unificato
client = genai.Client(api_key=CHIAVE_API)

print("Ricerca dei modelli Gemini testuali...\n")
print("-" * 60)

# Otteniamo i modelli
modelli = client.models.list()
conteggio = 0

for model in modelli:
    # Usiamo getattr per estrarre il nome in modo sicuro.
    # Se per qualche motivo manca, restituisce una stringa vuota invece di crashare.
    nome_grezzo = getattr(model, 'name', '')
    nome_pulito = nome_grezzo.replace('models/', '')
    
    # Poiché l'attributo sui metodi supportati al momento causa errori nel nuovo SDK,
    # filtriamo intelligentemente in base al nome: tutti i modelli "gemini" generano testo.
    if 'gemini' in nome_pulito.lower():
        conteggio += 1
        
        # Usiamo di nuovo getattr() per tutti i campi. 
        # È una best practice in Python quando si lavora con API esterne instabili.
        display_name = getattr(model, 'display_name', 'N/D')
        input_limit = getattr(model, 'input_token_limit', 'N/D')
        output_limit = getattr(model, 'output_token_limit', 'N/D')
        
        print(f"Nome API: {nome_pulito}")
        print(f"Display Name: {display_name}")
        print(f"Max Token in Input: {input_limit}")
        print(f"Max Token in Output: {output_limit}")
        print("-" * 60)

print(f"✅ Trovati {conteggio} modelli Gemini compatibili.")