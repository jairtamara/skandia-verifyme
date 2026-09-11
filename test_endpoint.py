from excel_loader import ExcelClientLoader
from open_finance import OpenFinanceValidator

of_loader = OpenFinanceValidator.of_loader
excel_loader = ExcelClientLoader()

try:
    clientes = excel_loader.obtener_todos()
    of_clientes = of_loader.obtener_todos()

    print(f"Clientes Skandia: {len(clientes)}")
    print(f"OF Clientes: {len(of_clientes)}")

    # Calcular valores REALES basados en datos
    en_open_finance = 0
    con_discrepancias = 0

    of_docs = set()
    for of_c in of_clientes:
        doc = str(of_c.get('numero_documento', '')).strip()
        if doc:
            of_docs.add(doc)

    print(f"OF docs (unique): {len(of_docs)}")

    for cliente in clientes:
        numero_doc = str(cliente.get('numero_documento', '')).strip()
        if numero_doc and numero_doc in of_docs:
            en_open_finance += 1
            # Verificar discrepancias
            resultado = OpenFinanceValidator.comparar_datos('', cliente)
            if resultado.get('hay_discrepancias', False):
                con_discrepancias += 1

    solo_skandia = len(clientes) - en_open_finance
    sincronizado = en_open_finance - con_discrepancias

    print(f"\nResultados:")
    print(f"  En Open Finance: {en_open_finance}")
    print(f"  Solo Skandia: {solo_skandia}")
    print(f"  Con Discrepancias: {con_discrepancias}")
    print(f"  Sincronizado: {sincronizado}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
