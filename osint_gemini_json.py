from google import genai
from google.genai import types
import os, json, target
 
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
 
config = types.GenerateContentConfig(
    system_instruction="""Sei un analista OSINT.
    Rispondi SOLO con un JSON valido, senza testo aggiuntivo.
    Non inventare dati non presenti nell'input.""",
    temperature=0.1,
    response_mime_type="application/json"
)
 
prompt = f"""
Analizza questi dati OSINT e restituisci un JSON con questa struttura:
{{
    "dominio": "il dominio analizzato",
    "tecnologie_rilevate": ["lista", "di", "tecnologie"],
    "email_trovate": [
        {{"email": "indirizzo", "ruolo_probabile": "ruolo", "rischio": "alto/medio/basso"}}
    ],
    "sottodomini": [
        {{"nome": "sub.dominio.com", "tipo": "web/mail/admin", "note": "osservazioni"}}
    ],
    "rischi_principali": [
        {{"descrizione": "descrizione rischio", "severita": "critica/alta/media/bassa"}}
    ],
    "prossimi_passi": ["lista", "azioni", "consigliate"]
}}
 
Dati:
{target.dominio} {target.dns_info} {target.whois_info[:1000]}
"""
 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=config
)
 
# Parsing del JSON
risultato = json.loads(response.text)
print(json.dumps(risultato, indent=2, ensure_ascii=False))