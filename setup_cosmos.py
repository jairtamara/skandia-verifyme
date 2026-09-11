#!/usr/bin/env python3
"""Setup script para crear base de datos y datos de prueba en Cosmos DB"""

import os
from datetime import datetime
from dotenv import load_dotenv
from cosmos_client import CosmosDB

load_dotenv()

# Datos de prueba
CLIENTES_PRUEBA = [
    {
        "id": "cliente_001",
        "nombre": "Carlos García López",
        "email": "carlos.garcia@email.com",
        "telefono": "+573101234567",
        "ciudad": "Bogotá",
        "actualizado_en": "2024-06-15",
        "requiere_actualizacion": False
    },
    {
        "id": "cliente_002",
        "nombre": "María Rodríguez Pérez",
        "email": "maria.rodriguez@email.com",
        "telefono": "+573159876543",
        "ciudad": "Medellín",
        "actualizado_en": "2023-01-10",
        "requiere_actualizacion": True,  # Este necesita actualización
        "razon_actualizacion": "Email rechazado - posible cambio de correo"
    },
    {
        "id": "cliente_003",
        "nombre": "Juan Pablo Martínez",
        "email": "juan.martinez@email.com",
        "telefono": "+573125554444",
        "ciudad": "Cali",
        "actualizado_en": "2025-02-20",
        "requiere_actualizacion": False
    }
]


def main():
    print("\n" + "="*60)
    print("SETUP: SKANDIA HACKATHON - META SIMULATOR")
    print("="*60 + "\n")

    try:
        # Conectar a Cosmos DB
        print("[INFO] Conectando a Cosmos DB...")
        db = CosmosDB()

        # Crear estructura
        print("\n[INFO] Creando base de datos y contenedor...")
        db.crear_base_datos_y_contenedor()

        # Insertar clientes de prueba
        print("\n[INFO] Insertando clientes de prueba...\n")
        for cliente in CLIENTES_PRUEBA:
            db.insertar_cliente(cliente)

        # Listar clientes
        print("\n[INFO] Clientes en la base de datos:")
        print("-" * 60)
        clientes = db.listar_todos_clientes()
        for c in clientes:
            estado = "[REQUIERE ACTUALIZACION]" if c.get("requiere_actualizacion") else "[ACTUALIZADO]"
            print(f"  * {c['nombre']:30} | {c['email']:30}")
            print(f"    {estado}")
            print()

        print("="*60)
        print("[OK] Setup completado exitosamente")
        print("="*60)
        print("\n[PROXIMOS PASOS]")
        print("  1. Instala dependencias:  pip install -r requirements.txt")
        print("  2. Inicia el servidor:    python app.py")
        print("  3. Abre en navegador:     http://localhost:8000")
        print("\n[USUARIO DE PRUEBA]")
        print(f"  Email: {CLIENTES_PRUEBA[1]['email']}")
        print(f"  (Este cliente tiene requiere_actualizacion=True)")
        print()

    except Exception as e:
        print(f"\n[ERROR] Error durante el setup: {e}")
        print("Verifica que COSMOS_URL y COSMOS_KEY esten configuradas en .env")
        exit(1)


if __name__ == "__main__":
    main()
