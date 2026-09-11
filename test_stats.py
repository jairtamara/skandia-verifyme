import requests

response = requests.get('http://localhost:8000/api/estadisticas-sincronizacion')
data = response.json()

print("ESTADISTICAS CORREGIDAS:")
print(f"  Total: {data.get('total')}")
print(f"  En Open Finance: {data.get('en_open_finance')}")
print(f"  Solo Skandia: {data.get('solo_skandia')}")
print(f"  Sincronizado (sin discrepancias): {data.get('sincronizado')}")
print(f"  Con Discrepancias: {data.get('con_discrepancias')}")
