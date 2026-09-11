import requests
import json

# Obtener datos del API
response = requests.get('http://localhost:8000/api/clientes/todos')
data = response.json()

clientes = data.get('clientes', [])

print("=" * 60)
print("VALIDACION API - /api/clientes/todos")
print("=" * 60)

# Contar estados
actualizado = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Actualizado')
pendiente = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Pendiente de actualizar')
vencido = sum(1 for c in clientes if c.get('estado_actualizacion') == 'Vencido')
requiere = sum(1 for c in clientes if c.get('requiere_actualizacion') == True)

print(f"\nTotal clientes: {len(clientes)}")
print(f"\nEstado de Vigencia:")
print(f"  Actualizado: {actualizado}")
print(f"  Pendiente: {pendiente}")
print(f"  Vencido: {vencido}")
print(f"\nRequiere Actualización (bool): {requiere}")

# Mostrar primeros 5 clientes como ejemplo
print(f"\nPrimeros 3 clientes (ejemplo):")
for i, c in enumerate(clientes[:3]):
    print(f"  [{i+1}] {c.get('nombre')}")
    print(f"      estado_actualizacion: {c.get('estado_actualizacion')}")
    print(f"      requiere_actualizacion: {c.get('requiere_actualizacion')}")

print("\n" + "=" * 60)
