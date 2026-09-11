from excel_loader import ExcelClientLoader
from open_finance_loader import OpenFinanceLoader

excel_loader = ExcelClientLoader()
of_loader = OpenFinanceLoader()

clientes = excel_loader.obtener_todos()
of_clientes = of_loader.obtener_todos()

print(f"Clientes Skandia: {len(clientes)}")
print(f"Clientes Open Finance: {len(of_clientes)}")

# Construir set de docs en OF
of_docs = set()
for of_c in of_clientes:
    doc = str(of_c.get('numero_documento', '')).strip()
    if doc:
        of_docs.add(doc)

print(f"Documentos en OF (unique): {len(of_docs)}")

# Contar cuantos de Skandia están en OF
en_of = 0
solo_skandia = 0

for cliente in clientes:
    numero_doc = str(cliente.get('numero_documento', '')).strip()
    if numero_doc:
        if numero_doc in of_docs:
            en_of += 1
        else:
            solo_skandia += 1

print(f"\nResultados:")
print(f"  En Open Finance: {en_of}")
print(f"  Solo Skandia: {solo_skandia}")
print(f"  Total: {en_of + solo_skandia}")
