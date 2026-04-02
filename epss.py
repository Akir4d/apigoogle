import requests
#import json
 
# Lista di CVE dal nostro scan Nessus
cve_list = [
    "CVE-2011-2523",   # vsftpd backdoor
    "CVE-2007-2447",   # Samba command injection
    "CVE-2014-0160",   # Heartbleed
    "CVE-2021-44228",  # Log4Shell
]
 
print(f"{'CVE':<20} {'EPSS':>8} {'Percentile':>12} {'Priorita'}")
print("-" * 60)
 
for cve in cve_list:
    resp = requests.get(
        f"https://api.first.org/data/v1/epss?cve={cve}"
    )
    data = resp.json()["data"]
    if data:
        epss = float(data[0]["epss"])
        pctl = float(data[0]["percentile"])
        if epss > 0.5:
            priority = "CRITICA"
        elif epss > 0.1:
            priority = "ALTA"
        else:
            priority = "MEDIA"
        print(f"{cve:<20} {epss:>8.4f} {pctl:>12.4f} {priority}")
