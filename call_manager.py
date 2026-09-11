"""Call Manager - Gestiona videollamadas con Jitsi

Utiliza Jitsi Meet (open source) para videollamadas
Sin costos, sin registros, privado y seguro
"""

import uuid
from datetime import datetime
from typing import Dict, List


class CallManager:
    """Gestor de videollamadas con Jitsi Meet

    En producción se conectaría a:
    - Jitsi servidor propio
    - Base de datos de llamadas
    - Webhooks para eventos de llamada
    """

    # Servidor Jitsi público (demo)
    JITSI_SERVER = "https://meet.jit.si"

    # Registro simulado de llamadas
    LLAMADAS_REGISTRO = []

    @staticmethod
    def generar_enlace_llamada(email: str, nombre_cliente: str, nombre_asesor: str = "Asesor Skandia") -> Dict:
        """Genera enlace de videollamada Jitsi

        Retorna:
        {
            "id_llamada": "call_xxx",
            "enlace": "https://meet.jit.si/skandia_xxx",
            "cliente_email": email,
            "cliente_nombre": nombre_cliente,
            "asesor_nombre": nombre_asesor,
            "fecha_inicio": timestamp,
            "estado": "pendiente",
            "duracion_segundos": 0
        }
        """

        # Generar ID único de llamada
        call_id = f"skandia_{uuid.uuid4().hex[:12]}"
        room_name = f"skandia-{email.split('@')[0]}-{uuid.uuid4().hex[:8]}"

        # Crear registro de llamada
        llamada = {
            "id_llamada": call_id,
            "room_name": room_name,
            "enlace": f"{CallManager.JITSI_SERVER}/{room_name}",
            "enlace_iframe": f"{CallManager.JITSI_SERVER}/{room_name}?userInfo.displayName={nombre_asesor}",
            "cliente_email": email,
            "cliente_nombre": nombre_cliente,
            "asesor_nombre": nombre_asesor,
            "fecha_inicio": datetime.now().isoformat(),
            "estado": "generada",
            "duracion_segundos": 0,
            "participantes": [nombre_asesor],
            "notas": ""
        }

        # Guardar en registro
        CallManager.LLAMADAS_REGISTRO.append(llamada)

        return llamada

    @staticmethod
    def enviar_invitacion(email: str, nombre_cliente: str, enlace: str) -> Dict:
        """Simula envío de invitación al cliente

        En producción:
        - Enviaría SMS/WhatsApp con enlace
        - Enviaría Email con instrucciones
        - Enviaría notificación push
        """

        return {
            "enviado": True,
            "canal": "SMS + Email",
            "mensaje": f"Hola {nombre_cliente}, tu asesor de Skandia te invita a una videollamada. Enlace: {enlace}",
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def registrar_inicio_llamada(id_llamada: str, nombre_cliente: str = None) -> Dict:
        """Registra el inicio de una llamada"""

        for llamada in CallManager.LLAMADAS_REGISTRO:
            if llamada["id_llamada"] == id_llamada:
                llamada["estado"] = "en_curso"
                llamada["fecha_inicio"] = datetime.now().isoformat()
                if nombre_cliente and nombre_cliente not in llamada["participantes"]:
                    llamada["participantes"].append(nombre_cliente)
                return llamada

        return None

    @staticmethod
    def registrar_fin_llamada(id_llamada: str, duracion_segundos: int, notas: str = "") -> Dict:
        """Registra el fin de una llamada y guarda datos actualizados"""

        for llamada in CallManager.LLAMADAS_REGISTRO:
            if llamada["id_llamada"] == id_llamada:
                llamada["estado"] = "completada"
                llamada["duracion_segundos"] = duracion_segundos
                llamada["fecha_fin"] = datetime.now().isoformat()
                llamada["notas"] = notas
                return llamada

        return None

    @staticmethod
    def obtener_historial_cliente(email: str) -> List[Dict]:
        """Obtiene historial de llamadas de un cliente"""

        return [
            l for l in CallManager.LLAMADAS_REGISTRO
            if l["cliente_email"].lower() == email.lower()
        ]

    @staticmethod
    def obtener_llamada(id_llamada: str) -> Dict:
        """Obtiene detalles de una llamada específica"""

        for llamada in CallManager.LLAMADAS_REGISTRO:
            if llamada["id_llamada"] == id_llamada:
                return llamada

        return None

    @staticmethod
    def generar_resumen_llamada(id_llamada: str, datos_actualizados: Dict) -> Dict:
        """Genera resumen de lo realizado en la llamada"""

        llamada = CallManager.obtener_llamada(id_llamada)

        if not llamada:
            return None

        return {
            "id_llamada": id_llamada,
            "cliente": llamada["cliente_nombre"],
            "asesor": llamada["asesor_nombre"],
            "duracion": f"{llamada['duracion_segundos'] // 60}m {llamada['duracion_segundos'] % 60}s",
            "fecha": llamada.get("fecha_inicio", ""),
            "participantes": llamada["participantes"],
            "datos_actualizados": datos_actualizados,
            "proximos_pasos": [
                "Validar datos con Open Finance",
                "Generar campaña publicitaria",
                "Enviar confirmación a cliente"
            ]
        }

    @staticmethod
    def listar_todas_llamadas() -> List[Dict]:
        """Lista todas las llamadas registradas"""

        return sorted(
            CallManager.LLAMADAS_REGISTRO,
            key=lambda x: x["fecha_inicio"],
            reverse=True
        )
