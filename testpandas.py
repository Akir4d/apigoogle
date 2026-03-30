import pandas as pd

# Leggi log CSV
df = pd.read_csv("auth.log.csv")

# Filtra solo eventi falliti
failed = df[df['message'].str.contains("Failed", na=False)].head(50) # inviamo i primi 50

# Raggruppa per IP
by_ip = failed.groupby('src_ip').size()

# Top 10 IP con più fallimenti
top_attackers = by_ip.nlargest(10)
print(top_attackers)