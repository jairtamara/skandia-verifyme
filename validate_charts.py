from excel_loader import ExcelClientLoader
from open_finance_loader import OpenFinanceLoader

# Cargar datos
loader_excel = ExcelClientLoader()
loader_of = OpenFinanceLoader()

clientes = loader_excel.obtener_todos()
clientes_of = loader_of.obtener_todos()

print("=" * 60)
print("VALIDACION DE GRAFICAS")
print("=" * 60)

# Grafica 1: Estado de Vigencia
print("\n1. ESTADO DE VIGENCIA:")
actualizado = sum(1 for c in clientes if loader_excel.obtener_estado_actualizacion(c) == 'Actualizado')
pendiente = sum(1 for c in clientes if loader_excel.obtener_estado_actualizacion(c) == 'Pendiente de actualizar')
vencido = sum(1 for c in clientes if loader_excel.obtener_estado_actualizacion(c) == 'Vencido')
print(f"  Actualizado: {actualizado}")
print(f"  Pendiente: {pendiente}")
print(f"  Vencido: {vencido}")

# Grafica 2: Cobertura Open Finance
print("\n2. COBERTURA OPEN FINANCE:")
localizados = 0
no_localizados = 0
for cliente in clientes:
    doc = cliente.get('numero_documento')
    if doc and loader_of.cliente_encontrado(doc):
        localizados += 1
    else:
        no_localizados += 1
print(f"  Localizados en OF: {localizados}")
print(f"  No localizados: {no_localizados}")

# Grafica 3: Estado de Notificaciones
print("\n3. ESTADO DE NOTIFICACIONES:")
requieren = sum(1 for c in clientes if c.get('estado_actualizacion') in ['Pendiente de actualizar', 'Vencido'])
print(f"  Requieren actualización: {requieren}")
print(f"  Distribucion:")
print(f"  -> Enviadas (30%): {int(requieren * 0.3)}")
print(f"  -> Pendientes (50%): {int(requieren * 0.5)}")
print(f"  -> En Proceso (20%): {int(requieren * 0.2)}")

# Grafica 4: Origen de Datos
print("\n4. ORIGEN DE DATOS:")
solo_skandia = sum(1 for c in clientes if not loader_of.cliente_encontrado(str(c.get('numero_documento', '')).strip()))
sincronizado = sum(1 for c in clientes if loader_of.cliente_encontrado(str(c.get('numero_documento', '')).strip()))
solo_of = len(clientes_of) - sincronizado
print(f"  Solo Skandia: {solo_skandia}")
print(f"  Solo Open Finance: {solo_of}")
print(f"  Sincronizado: {sincronizado}")

print("\n" + "=" * 60)
print(f"TOTAL: {len(clientes)}")
print("=" * 60)
