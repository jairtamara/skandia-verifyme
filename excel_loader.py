from openpyxl import load_workbook
from datetime import datetime
import os

class ExcelClientLoader:
    def __init__(self, filename="Base_Clientes_Actualizacion_Datos_IA.xlsx"):
        self.filename = filename
        self.clientes = []
        self.load_data()

    def load_data(self):
        """Carga los datos desde el archivo Excel"""
        if not os.path.exists(self.filename):
            print(f"Error: {self.filename} no encontrado")
            return

        try:
            wb = load_workbook(self.filename)
            ws = wb['Clientes']

            # Saltar encabezado en fila 2 (que contiene los nombres de columnas)
            for row_idx in range(3, ws.max_row + 1):
                cliente_data = {}

                # Mapeo de columnas (A=1, B=2, etc.)
                cliente_data['id'] = ws.cell(row_idx, 1).value
                cliente_data['tipo_documento'] = ws.cell(row_idx, 2).value
                cliente_data['numero_documento'] = ws.cell(row_idx, 3).value
                cliente_data['nombre'] = ws.cell(row_idx, 4).value
                cliente_data['telefono'] = ws.cell(row_idx, 5).value
                cliente_data['email'] = ws.cell(row_idx, 6).value
                cliente_data['ciudad'] = ws.cell(row_idx, 7).value
                cliente_data['direccion'] = ws.cell(row_idx, 8).value
                cliente_data['fecha_registro'] = ws.cell(row_idx, 9).value
                cliente_data['fecha_ultima_actualizacion'] = ws.cell(row_idx, 10).value
                cliente_data['responsable'] = ws.cell(row_idx, 12).value
                cliente_data['observaciones'] = ws.cell(row_idx, 13).value
                cliente_data['productos'] = ws.cell(row_idx, 14).value
                cliente_data['score_crediticio'] = ws.cell(row_idx, 15).value

                # Agregar TODOS los clientes (incluso sin nombre o documento)
                # Solo saltar si la fila está completamente vacía
                if cliente_data.get('nombre') or cliente_data.get('numero_documento') or cliente_data.get('email'):
                    self.clientes.append(cliente_data)

            print(f"Cargados {len(self.clientes)} clientes desde Excel (TODOS los registros)")
        except Exception as e:
            print(f"Error al cargar Excel: {e}")

    def buscar_por_email(self, email):
        """Busca un cliente por email"""
        for cliente in self.clientes:
            if cliente['email'] and cliente['email'].lower() == email.lower():
                return cliente
        return None

    def buscar_por_documento(self, numero_documento):
        """Busca un cliente por número de documento"""
        for cliente in self.clientes:
            if cliente['numero_documento'] and str(cliente['numero_documento']).strip() == str(numero_documento).strip():
                return cliente
        return None

    def obtener_todos(self):
        """Retorna todos los clientes"""
        return self.clientes

    def obtener_estado_actualizacion(self, cliente):
        """Determina el estado de actualización del cliente"""
        fecha_ultima = cliente.get('fecha_ultima_actualizacion')

        if not fecha_ultima:
            return 'Sin fecha de actualizacion'

        try:
            if isinstance(fecha_ultima, str):
                fecha_ultima = datetime.fromisoformat(fecha_ultima.replace('T', ' ').split('.')[0])

            hoy = datetime.now()
            dias_desde_actualizacion = (hoy - fecha_ultima).days

            if dias_desde_actualizacion <= 365:
                return 'Actualizado'
            elif dias_desde_actualizacion <= 450:
                return 'Pendiente de actualizar'
            else:
                return 'Vencido'
        except:
            return 'Error en fecha'

    def actualizar_cliente(self, email, datos):
        """Actualiza un cliente en memoria (para demo)"""
        cliente = self.buscar_por_email(email)
        if cliente:
            cliente.update(datos)
            cliente['fecha_ultima_actualizacion'] = datetime.now()
            return True
        return False
