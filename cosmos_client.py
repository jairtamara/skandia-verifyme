import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

COSMOS_URL = os.getenv("COSMOS_URL")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE", "skandia_hackathon")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER", "clientes")


class CosmosDB:
    def __init__(self):
        self.client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
        self.database = self.client.get_database_client(DATABASE_NAME)
        self.container = self.database.get_container_client(CONTAINER_NAME)

    def crear_base_datos_y_contenedor(self):
        """Crea base de datos y contenedor si no existen"""
        try:
            # Crear base de datos
            self.client.create_database_if_not_exists(id=DATABASE_NAME)
            print(f"[OK] Base de datos '{DATABASE_NAME}' lista")

            # Crear contenedor
            self.database.create_container_if_not_exists(
                id=CONTAINER_NAME,
                partition_key=PartitionKey(path="/email")
            )
            print(f"[OK] Contenedor '{CONTAINER_NAME}' listo")
        except Exception as e:
            print(f"[ERROR] Error creando estructura: {e}")
            raise

    def obtener_cliente_por_email(self, email: str):
        """Obtiene un cliente por email"""
        try:
            query = "SELECT * FROM c WHERE c.email = @email"
            items = list(self.container.query_items(
                query=query,
                parameters=[{"name": "@email", "value": email}]
            ))
            return items[0] if items else None
        except Exception as e:
            print(f"[ERROR] Error obteniendo cliente: {e}")
            return None

    def obtener_cliente_por_id(self, client_id: str, email: str):
        """Obtiene un cliente por ID (requiere email como partition key)"""
        try:
            item = self.container.read_item(item=client_id, partition_key=email)
            return item
        except Exception as e:
            print(f"[ERROR] Error obteniendo cliente: {e}")
            return None

    def insertar_cliente(self, cliente: dict):
        """Inserta un nuevo cliente"""
        try:
            self.container.create_item(body=cliente)
            print(f"[OK] Cliente {cliente.get('email')} insertado")
        except Exception as e:
            print(f"[ERROR] Error insertando cliente: {e}")
            raise

    def actualizar_cliente(self, client_id: str, email: str, datos_actualizacion: dict):
        """Actualiza datos de un cliente"""
        try:
            cliente = self.obtener_cliente_por_id(client_id, email)
            if cliente:
                cliente.update(datos_actualizacion)
                self.container.upsert_item(cliente)
                print(f"[OK] Cliente {email} actualizado")
                return cliente
            else:
                print(f"[ERROR] Cliente no encontrado")
                return None
        except Exception as e:
            print(f"[ERROR] Error actualizando cliente: {e}")
            return None

    def listar_todos_clientes(self):
        """Lista todos los clientes"""
        try:
            query = "SELECT * FROM c"
            items = list(self.container.query_items(query=query))
            return items
        except Exception as e:
            print(f"[ERROR] Error listando clientes: {e}")
            return []
