"""Open Finance Validator - MVP Demo

Valida datos financieros via Open Finance usando datos simulados.
En producción se conectaría a agregadores regulados de Open Finance.
"""

import random
from typing import Dict, List
from datetime import datetime
from open_finance_loader import OpenFinanceLoader


class OpenFinanceValidator:
    """MVP: Consulta datos reales de Open Finance desde Excel

    En producción:
    - Conectaría a agregadores de datos (Plaid, Belvo, etc)
    - Consultaría saldo, movimientos, ingresos
    - Verificaría información vs BD
    - Requeriría consentimiento expreso del cliente
    """

    # Cargar datos desde Open Finance Excel
    of_loader = OpenFinanceLoader()

    @staticmethod
    def validar_open_finance(email: str, cliente_data: dict = None) -> Dict:
        """Valida datos via Open Finance usando datos reales del Excel

        En producción:
        1. Pedir consentimiento al cliente
        2. Conectar a Open Finance API
        3. Validar tokens de acceso
        4. Comparar datos con BD interna
        5. Generar reporte de discrepancias
        """

        # Obtener número de documento del cliente
        numero_documento = cliente_data.get("numero_documento") if cliente_data else None

        if not numero_documento:
            return {
                "acceso_otorgado": False,
                "datos_obtenidos": None,
                "validaciones": [],
                "fecha_consulta": datetime.now().isoformat(),
                "requiere_actualizacion": False,
                "mensaje": "No se puede consultar Open Finance sin número de documento"
            }

        # Buscar datos en Open Finance
        datos_of = OpenFinanceValidator.of_loader.obtener_datos_resumidos(numero_documento)

        if datos_of:
            # Simular validaciones
            validaciones = OpenFinanceValidator._ejecutar_validaciones(
                datos_of,
                cliente_data
            )

            return {
                "acceso_otorgado": True,
                "datos_obtenidos": {
                    "nombre": datos_of.get("nombre"),
                    "email": datos_of.get("email"),
                    "bancos": [],  # Compatibilidad con HTML anterior
                    "saldo": datos_of.get("saldo_total", 0),
                    "ingresos_mensuales": datos_of.get("ingresos_mensuales", 0),
                    "score_crediticio": datos_of.get("score_crediticio", 0),
                    "productos": datos_of.get("productos", []) if isinstance(datos_of.get("productos"), list) else [],
                    "riesgo": datos_of.get("riesgo", "MEDIO"),
                    "deuda_vigente": datos_of.get("deuda_vigente", 0),
                    "tiene_mora": datos_of.get("tiene_mora", False),
                    "estado_cuenta": datos_of.get("estado_cuenta", "DESCONOCIDO")
                },
                "validaciones": validaciones,
                "fecha_consulta": datetime.now().isoformat(),
                "requiere_actualizacion": len(
                    [v for v in validaciones if not v["valido"]]
                ) > 0,
                "mensaje": OpenFinanceValidator._generar_mensaje(validaciones)
            }

        # Cliente sin datos en Open Finance
        return {
            "acceso_otorgado": False,
            "datos_obtenidos": None,
            "validaciones": [],
            "fecha_consulta": datetime.now().isoformat(),
            "requiere_actualizacion": False,
            "mensaje": "No se encontraron datos en Open Finance. El cliente podria no tener productos financieros vinculados."
        }

    @staticmethod
    def _ejecutar_validaciones(datos_finance: Dict, cliente_data: Dict) -> list:
        """Ejecuta validaciones de datos"""

        validaciones = [
            {
                "concepto": "Actividad Reciente",
                "valido": True,
                "detalle": f"Ultima transaccion: {datos_finance.get('fecha_ultima_transaccion', 'N/A')}"
            },
            {
                "concepto": "Score Crediticio",
                "valido": datos_finance.get("score_crediticio", 0) >= 600,
                "detalle": f"Score: {datos_finance.get('score_crediticio', 0)}/850"
            },
            {
                "concepto": "Saldo Disponible",
                "valido": datos_finance.get("saldo_total", 0) > 0,
                "detalle": f"Saldo: ${datos_finance.get('saldo_total', 0):,.0f}"
            },
            {
                "concepto": "Riesgo de Credito",
                "valido": datos_finance.get("riesgo", "MEDIO").upper() in ["BAJO", "MEDIO"],
                "detalle": f"Nivel de riesgo: {datos_finance.get('riesgo', 'MEDIO').upper()}"
            },
            {
                "concepto": "Estado Cuenta",
                "valido": datos_finance.get("estado_cuenta") == "ACTIVA",
                "detalle": f"Estado: {datos_finance.get('estado_cuenta', 'DESCONOCIDO')}"
            },
            {
                "concepto": "Sin Mora",
                "valido": not datos_finance.get("tiene_mora", False),
                "detalle": f"Dias en mora: {datos_finance.get('dias_mora', 0)}"
            }
        ]

        return validaciones

    @staticmethod
    def _generar_mensaje(validaciones: list) -> str:
        """Genera mensaje basado en validaciones"""

        validas = sum(1 for v in validaciones if v["valido"])
        total = len(validaciones)

        if validas == total:
            return "Todos los datos fueron validados exitosamente via Open Finance."
        else:
            invalidas = total - validas
            return f"Se encontraron {invalidas} discrepancia(s) en los datos. Se requiere actualizacion."

    @staticmethod
    def comparar_datos(email: str, cliente_data: dict) -> Dict:
        """Compara datos de Skandia vs Open Finance

        Retorna discrepancias encontradas:
        - Datos en Skandia
        - Datos en Open Finance
        - Diferencias
        """

        numero_documento = cliente_data.get("numero_documento")

        # Datos actuales en Skandia
        datos_skandia = {
            "email": cliente_data.get("email", ""),
            "nombre": cliente_data.get("nombre", ""),
            "telefono": cliente_data.get("telefono", "No registrado"),
            "ciudad": cliente_data.get("ciudad", "No registrada"),
            "score_crediticio": cliente_data.get("score_crediticio", "N/A"),
            "actualizado_en": cliente_data.get("fecha_ultima_actualizacion", "Desconocido")
        }

        # Buscar datos en Open Finance
        datos_of = OpenFinanceValidator.of_loader.obtener_datos_resumidos(numero_documento)

        if datos_of:
            datos_open_finance = {
                "nombre": datos_of.get("nombre", ""),
                "saldo": datos_of.get("saldo_total", 0),
                "ingresos_mensuales": datos_of.get("ingresos_mensuales", 0),
                "score_crediticio": datos_of.get("score_crediticio", 0),
                "riesgo": datos_of.get("riesgo", "MEDIO"),
                "productos": datos_of.get("productos", []),
                "estado_cuenta": datos_of.get("estado_cuenta", "DESCONOCIDO"),
                "tiene_mora": datos_of.get("tiene_mora", False)
            }

            # Comparar SOLO en los 4 campos solicitados
            discrepancias = []

            # 1. TELEFONO - Solo si AMBAS bases lo tienen
            telefono_skandia = cliente_data.get("telefono", "").strip()
            # Open Finance no tiene teléfono, así que no mostrar discrepancia
            # Mantener los datos de Skandia como está

            # 2. CORREO ELECTRONICO - Solo si AMBAS bases lo tienen
            email_skandia = cliente_data.get("email", "").strip()
            email_of = datos_of.get("email", "").strip()

            # Solo mostrar discrepancia si AMBAS bases tienen correo y son diferentes
            if email_skandia and email_of and email_skandia != email_of:
                discrepancias.append({
                    "campo": "Correo Electronico",
                    "valor_skandia": email_skandia,
                    "valor_open_finance": email_of,
                    "tipo_diferencia": "Email desincronizado",
                    "prioridad": "alta",
                    "accion_recomendada": "Actualizar email del cliente con la información más reciente de Open Finance"
                })

            # 3. DIRECCION - Solo si AMBAS bases lo tienen
            direccion_skandia = cliente_data.get("direccion", "").strip()
            # Open Finance no tiene dirección, así que no mostrar discrepancia
            # Mantener los datos de Skandia como está

            # 4. VIGENCIA - Comparar estado de actualización
            fecha_ultima = cliente_data.get("fecha_ultima_actualizacion")
            estado_vigencia = "Desconocido"

            if fecha_ultima:
                try:
                    if isinstance(fecha_ultima, str):
                        from datetime import datetime
                        fecha_ultima = datetime.fromisoformat(fecha_ultima.replace('T', ' ').split('.')[0])

                    hoy = datetime.now() if isinstance(datetime, type) else __import__('datetime').datetime.now()
                    dias_desde_actualizacion = (hoy - fecha_ultima).days

                    if dias_desde_actualizacion <= 30:
                        estado_vigencia = "Actualizado"
                    elif dias_desde_actualizacion <= 365:
                        estado_vigencia = "Pendiente de actualizar"
                    else:
                        estado_vigencia = "Vencido"
                except:
                    estado_vigencia = "Error en fecha"

            # Mostrar vigencia como información
            # (No es una discrepancia, sino un estado)
            if estado_vigencia == "Vencido" or estado_vigencia == "Pendiente de actualizar":
                discrepancias.append({
                    "campo": "Vigencia",
                    "valor_skandia": estado_vigencia,
                    "valor_open_finance": "Requiere actualización",
                    "tipo_diferencia": "Estado de datos desactualizado",
                    "prioridad": "alta" if estado_vigencia == "Vencido" else "media",
                    "accion_recomendada": f"Contactar al cliente para actualizar su información. Datos no actualizados hace más de {max(30, dias_desde_actualizacion)} días"
                })

            return {
                "hay_discrepancias": len(discrepancias) > 0,
                "total_discrepancias": len(discrepancias),
                "datos_skandia": datos_skandia,
                "datos_open_finance": datos_open_finance,
                "discrepancias": discrepancias,
                "resumen": f"Se encontraron {len(discrepancias)} discrepancia(s) entre los datos de Skandia y Open Finance"
            }

        return {
            "hay_discrepancias": False,
            "total_discrepancias": 0,
            "datos_skandia": datos_skandia,
            "datos_open_finance": None,
            "discrepancias": [],
            "resumen": "No se encontraron datos en Open Finance para comparar"
        }
