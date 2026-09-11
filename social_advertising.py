"""Social Advertising - MVP Demo

Simula envio de publicidad a través de redes sociales (Instagram, Facebook, WhatsApp)
En producción se conectaría a APIs de Meta, WhatsApp Business API, etc.
"""

import random
from datetime import datetime
from typing import Dict, List


class SocialAdvertising:
    """MVP: Simula campanas publicitarias en redes sociales

    En producción:
    - Meta Ads API (Facebook, Instagram)
    - WhatsApp Business API
    - SMS (Twilio)
    - Email Marketing
    - Push Notifications
    """

    CANALES_DISPONIBLES = ["instagram", "facebook", "whatsapp", "email", "sms"]

    # Plantillas de mensajes segun el tipo de validacion fallida
    PLANTILLAS_MENSAJES = {
        "vigencia_fallecida": {
            "instagram": "Hola! Notamos un inconveniente en tu perfil de Skandia. Por favor contacta a nuestro equipo de atencion al cliente.",
            "facebook": "Hola! Necesitamos actualizar tu información. Entra a tu cuenta de Skandia o contactanos.",
            "whatsapp": "Hola! Tenemos una actualización importante para tu cuenta. Responde este mensaje.",
            "email": "Verificación de Cuenta - Acción Requerida",
            "sms": "Skandia: Necesitamos actualizar tu información. Ingresa a tu cuenta o contactanos."
        },
        "open_finance_discrepancia": {
            "instagram": "Hola! Detectamos cambios en tus datos financieros. Actualiza tu informacion personal en Skandia.",
            "facebook": "Tu perfil necesita actualizacion. Verificamos cambios en tus datos. Entra a tu cuenta Skandia.",
            "whatsapp": "Skandia: Detectamos cambios en tu información. Necesitamos que la actualices.",
            "email": "Actualización Requerida - Datos Personales",
            "sms": "Skandia: Actualiza tu información. Ingresa ahora a tu cuenta."
        },
        "datos_desactualizados": {
            "instagram": "Tu información en Skandia está desactualizada. Actualicemos juntos tus datos personales.",
            "facebook": "Mantén tu perfil actualizado. Haz clic para actualizar tu información ahora.",
            "whatsapp": "Hola! Es momento de actualizar tu información personal en Skandia.",
            "email": "Actualización de Información Personal",
            "sms": "Skandia: Actualiza tu perfil ahora. Solo te toma 2 minutos."
        }
    }

    @staticmethod
    def generar_campana(
        email: str,
        cliente_data: dict,
        razon: str,
        validaciones_fallidas: List[Dict] = None
    ) -> Dict:
        """Genera campana publicitaria multi-canal

        razon: 'vigencia_fallecida' | 'open_finance_discrepancia' | 'datos_desactualizados'
        """

        if validaciones_fallidas is None:
            validaciones_fallidas = []

        nombre_cliente = cliente_data.get("nombre", "Cliente").split()[0]

        # Seleccionar canales optimos (demo)
        canales = SocialAdvertising._seleccionar_canales(cliente_data)

        # Generar mensajes por canal
        campana = {
            "email": email,
            "cliente": nombre_cliente,
            "razon": razon,
            "fecha_generacion": datetime.now().isoformat(),
            "canales": [],
            "presupuesto_estimado": len(canales) * 5000,  # COP simulado
            "validaciones_fallidas": validaciones_fallidas
        }

        for canal in canales:
            mensaje = SocialAdvertising._generar_mensaje(
                nombre_cliente,
                razon,
                canal
            )

            campana["canales"].append({
                "canal": canal,
                "mensaje": mensaje,
                "estado": "pendiente_envio",
                "objetivo": SocialAdvertising._generar_objetivo(canal),
                "audiencia": SocialAdvertising._generar_audiencia(cliente_data, canal)
            })

        return campana

    @staticmethod
    def _seleccionar_canales(cliente_data: dict) -> List[str]:
        """Selecciona canales segun perfil del cliente"""

        canales = []

        # Siempre incluir email
        canales.append("email")

        # Si tiene perfil en redes (simulado)
        if random.random() > 0.3:
            canales.append("instagram")

        if random.random() > 0.3:
            canales.append("facebook")

        # WhatsApp es efectivo
        if random.random() > 0.2:
            canales.append("whatsapp")

        # SMS complementario
        if random.random() > 0.5:
            canales.append("sms")

        return list(set(canales))  # Eliminar duplicados

    @staticmethod
    def _generar_mensaje(nombre: str, razon: str, canal: str) -> str:
        """Genera mensaje personalizado segun canal"""

        plantilla = SocialAdvertising.PLANTILLAS_MENSAJES.get(
            razon,
            SocialAdvertising.PLANTILLAS_MENSAJES["datos_desactualizados"]
        )

        mensaje = plantilla.get(canal, "Por favor actualiza tu información.")

        # Personalizacion segun canal
        if canal == "instagram":
            return f"{nombre}, {mensaje}"
        elif canal == "facebook":
            return f"Hola {nombre}! {mensaje}"
        elif canal == "whatsapp":
            return f"Hola {nombre}! {mensaje} 👋"
        elif canal == "sms":
            return mensaje
        else:  # email
            return mensaje

    @staticmethod
    def _generar_objetivo(canal: str) -> Dict:
        """Define objetivo de la campana por canal"""

        objetivos = {
            "instagram": {
                "tipo": "Awareness",
                "impresiones_estimadas": 5000,
                "ctr_esperado": 3.5,
                "cpc": 1500
            },
            "facebook": {
                "tipo": "Engagement",
                "impresiones_estimadas": 8000,
                "ctr_esperado": 2.8,
                "cpc": 1200
            },
            "whatsapp": {
                "tipo": "Conversion",
                "impresiones_estimadas": 100,
                "ctr_esperado": 45.0,
                "cpc": 5000
            },
            "email": {
                "tipo": "Direct",
                "impresiones_estimadas": 1,
                "ctr_esperado": 25.0,
                "cpc": 0
            },
            "sms": {
                "tipo": "Urgency",
                "impresiones_estimadas": 1,
                "ctr_esperado": 15.0,
                "cpc": 500
            }
        }

        return objetivos.get(canal, objetivos["email"])

    @staticmethod
    def _generar_audiencia(cliente_data: dict, canal: str) -> Dict:
        """Define audiencia segun datos del cliente"""

        ciudad = cliente_data.get("ciudad", "Bogota")
        edad_simulada = random.randint(25, 65)

        return {
            "ubicacion": ciudad,
            "edad_aproximada": edad_simulada,
            "segmento": "Clientes Activos",
            "interes_principal": "Servicios Financieros",
            "dispositivo": "Mobile" if random.random() > 0.3 else "Desktop"
        }

    @staticmethod
    def simular_envio(campana: Dict) -> Dict:
        """Simula el envio de la campana"""

        resultados = {
            "campana_id": f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "email_cliente": campana["email"],
            "cliente": campana["cliente"],
            "fecha_envio": datetime.now().isoformat(),
            "total_mensajes": len(campana["canales"]),
            "detalle_envios": []
        }

        for canal_config in campana["canales"]:
            # Simular envio (90% exitoso)
            exitoso = random.random() > 0.1

            resultados["detalle_envios"].append({
                "canal": canal_config["canal"],
                "estado": "enviado" if exitoso else "fallido",
                "timestamp": datetime.now().isoformat(),
                "razon_fallo": None if exitoso else "Conexion temporal rechazada"
            })

        resultados["total_exitosos"] = sum(
            1 for d in resultados["detalle_envios"] if d["estado"] == "enviado"
        )

        return resultados

    @staticmethod
    def _generar_proximos_pasos(resultado_vigencia: Dict, resultado_open_finance: Dict) -> list:
        """Genera proximos pasos basado en validaciones"""

        pasos = []

        if not resultado_vigencia["vigente"]:
            pasos.append("Contactar familia o apoderado legal")
            return pasos

        if not resultado_open_finance["acceso_otorgado"]:
            pasos.append("Solicitar vinculacion de productos financieros")
            pasos.append("Verificar datos de identidad")
        else:
            if resultado_open_finance.get("requiere_actualizacion"):
                pasos.append("Cliente debe actualizar informacion personal")
                pasos.append("Validar datos contra Open Finance")
            else:
                pasos.append("Ofrecer productos personalizados")
                pasos.append("Actualizar estado en base de datos")

        pasos.append("Enviar confirmacion de actualizacion")

        return pasos
