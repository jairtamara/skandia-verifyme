import requests

print("="*70)
print("VALIDACION COMPLETA DE GRAFICAS")
print("="*70)

# Obtener datos
response_clientes = requests.get('http://localhost:8000/api/clientes/todos')
response_stats = requests.get('http://localhost:8000/api/estadisticas-sincronizacion')

clientes = response_clientes.json().get('clientes', [])
stats = response_stats.json()

print("\nGRAFICA 1: ESTADO DE VIGENCIA")
print("-" * 70)
actualizado = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Actualizado')
pendiente = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Pendiente de actualizar')
vencido = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Vencido')
print(f"  Actualizado: {actualizado} (esperado: 39)")
print(f"  Pendiente: {pendiente} (esperado: 11)")
print(f"  Vencido: {vencido} (esperado: 2)")
if actualizado == 39 and pendiente == 11 and vencido == 2:
    print("  CORRECTO")
else:
    print("  ERROR")

print("\nGRAFICA 2: COBERTURA OPEN FINANCE")
print("-" * 70)
localizados = stats.get('en_open_finance', 0)
no_localizados = stats.get('solo_skandia', 0)
print(f"  Localizados: {localizados} (esperado: 52)")
print(f"  No localizados: {no_localizados} (esperado: 0)")
if localizados == 52 and no_localizados == 0:
    print("  CORRECTO")
else:
    print("  ERROR")

print("\nGRAFICA 3: ESTADO DE NOTIFICACIONES")
print("-" * 70)
requieren = sum(1 for c in clientes if c.get('requiere_actualizacion'))
enviadas = int(requieren * 0.3)
pendientes = int(requieren * 0.5)
en_proceso = int(requieren * 0.2)
print(f"  Requieren actualización (total): {requieren} (esperado: 13)")
print(f"  Distribucion (30%-50%-20%):")
print(f"    - Enviadas (30%): {enviadas}")
print(f"    - Pendientes (50%): {pendientes}")
print(f"    - En Proceso (20%): {en_proceso}")
if requieren == 13:
    print("  CORRECTO")
else:
    print("  ERROR")

print("\nGRAFICA 4: ORIGEN DE DATOS")
print("-" * 70)
solo_skandia = stats.get('solo_skandia', 0)
sincronizado = stats.get('sincronizado', 0)
con_discrepancias = stats.get('con_discrepancias', 0)
en_of = stats.get('en_open_finance', 0)
print(f"  Solo Skandia: {solo_skandia} (esperado: 0)")
print(f"  Sincronizado (sin discrepancias): {sincronizado}")
print(f"  Con Discrepancias: {con_discrepancias}")
print(f"  En Open Finance: {en_of} (esperado: 52)")
print(f"  Suma: {solo_skandia + sincronizado + con_discrepancias} (esperado: 52)")
if solo_skandia + sincronizado + con_discrepancias == 52:
    print("  CORRECTO")
else:
    print("  ERROR")

print("\n" + "="*70)
print("RESUMEN")
print("="*70)
print(f"Total clientes: {len(clientes)} (esperado: 52)")
print(f"Requieren actualización: {requieren}/52")
print(f"Actualizados: {actualizado}/52")
