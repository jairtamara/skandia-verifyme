from open_finance_loader import OpenFinanceLoader

of = OpenFinanceLoader()
print(f"Registros en Open Finance: {len(of.obtener_todos())}")
print("Primeros 5:")
for i, c in enumerate(of.obtener_todos()[:5]):
    print(f"  {i+1}. {c.get('numero_documento')} - {c.get('nombre')}")
