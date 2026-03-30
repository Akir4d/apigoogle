import subprocess
 
def raccogli_dns(dominio):
    """Esegue dig e restituisce i risultati"""
    risultato = subprocess.run(
        ["dig", dominio, "ANY", "+short"],
        capture_output=True, text=True
    )
    return risultato.stdout
 
def raccogli_whois(dominio):
    """Esegue whois e restituisce i risultati"""
    risultato = subprocess.run(
        ["whois", dominio],
        capture_output=True, text=True
    )
    return risultato.stdout
# Uso
dominio = "target.com"
dns_info = raccogli_dns(dominio)
whois_info = raccogli_whois(dominio)
 
# Scrittura su file target.py
with open("target.py", "w", encoding="utf-8") as f:
    f.write(f"dominio = '{dominio}'\n\n")
    f.write(f"dns_info = '''{dns_info}'''\n\n")
    f.write(f"whois_info = '''{whois_info}'''\n")

print("Dati salvati con successo in target.py")
