import pandas as pd
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 0.2,      # 0=deterministico, 1=creativo
    "max_output_tokens": 1024,
    "top_p": 0.8,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

# 1. Carica e filtra
df = pd.read_csv("auth.log.csv")
suspicious = df[df['message'].str.contains("Failed", na=False)]

# 2. Converti in stringa per l'AI
log_text = suspicious.head(100).to_string() #dobbiamo limitare a max 1000 righe

# 3. Analizza con AI
prompt = f"""
Analizza questi log e rispondi SOLO con JSON valido:
{{
  "anomalies": [
    {{
      "type": "brute_force",
      "src_ip": "...",
      "severity": "HIGH",
      "action": "Block IP"
    }}
  ]
}}

Log:
{log_text}
"""
response = model.generate_content(prompt)

print(response.text)