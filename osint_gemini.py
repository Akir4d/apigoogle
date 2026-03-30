from google import genai
from google.genai import types
import os, target # questo è il file target.py che abbiamo salvato prima
 
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
# Dati raccolti nello step precedente
dati_osint = f"""
DOMINIO: {target.dominio}
 
DNS RECORDS:
{target.dns_info}
 
WHOIS (estratto):
{target.whois_info[:1000]}
"""
# Configurazione: temperatura bassa = precisione
config = types.GenerateContentConfig(
    system_instruction="""Sei un analista OSINT esperto.
    Analizza SOLO le informazioni fornite, non inventare dati.
    Se un'informazione non è presente, scrivi 'Non disponibile'.""",
    temperature=0.2
)
 
prompt = f"""
Analizza i seguenti dati OSINT raccolti su un target.
Per ogni dato identificato, indica:
1. Informazione trovata
2. Rilevanza per la sicurezza (alta/media/bassa)
3. Possibili rischi
 
Dati:
{dati_osint}
 
Rispondi in formato tabella Markdown.
"""
 
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    config=config
)
print(response.text)
