"""Validador de Vigencia - Verifica si el cliente está activo/vivo"""

from enum import Enum
from typing import Dict, Tuple


class EstadoVigencia(Enum):
    ACTIVO = "activo"
    FALLECIDO = "fallecido"
    INACTIVO = "inactivo"
    NO_ENCONTRADO = "no_encontrado"


class VigenciaValidator:
    """MVP: Simula consulta a registros de defunciones y vigencia

    En producción, se conectaría a:
    - RUES (Registro Único de Personas)
    - Registro Civil (defunciones)
    - DIAN
    """

    # Base de datos simulada de defunciones y estados
    REGISTRO_DEFUNCIONES = {
        "fallecido_001@email.com": {
            "nombre": "Juan Perez Garcia",
            "estado": EstadoVigencia.FALLECIDO,
            "fecha_defuncion": "2024-03-15"
        }
    }

    REGISTRO_INACTIVOS = {
        "inactivo_001@email.com": {
            "nombre": "Pedro Rodriguez Lopez",
            "estado": EstadoVigencia.INACTIVO,
            "razon": "Falta de movimiento por 2 anos"
        }
    }

    @staticmethod
    def validar_vigencia(email: str, cliente_data: dict = None) -> Dict:
        """Valida si el cliente está vivo y activo

        Returns:
            {
                "vigente": bool,
                "estado": EstadoVigencia,
                "razon": str,
                "puede_continuar": bool,
                "mensaje": str
            }
        """

        email_lower = email.lower()

        # Verificar si está en registro de defunciones
        if email_lower in VigenciaValidator.REGISTRO_DEFUNCIONES:
            registro = VigenciaValidator.REGISTRO_DEFUNCIONES[email_lower]
            return {
                "vigente": False,
                "estado": EstadoVigencia.FALLECIDO.value,
                "razon": f"Registro de defuncion: {registro['fecha_defuncion']}",
                "puede_continuar": False,
                "mensaje": f"Lamentamos informar que {registro['nombre']} aparece en el registro de defunciones. Contacte con nuestro equipo de atencion al cliente."
            }

        # Verificar si está inactivo
        if email_lower in VigenciaValidator.REGISTRO_INACTIVOS:
            registro = VigenciaValidator.REGISTRO_INACTIVOS[email_lower]
            return {
                "vigente": False,
                "estado": EstadoVigencia.INACTIVO.value,
                "razon": registro['razon'],
                "puede_continuar": True,  # Puede reactivarse
                "mensaje": f"La cuenta de {registro['nombre']} ha estado inactiva. Procedemos a reactivarla."
            }

        # Cliente activo
        if cliente_data:
            return {
                "vigente": True,
                "estado": EstadoVigencia.ACTIVO.value,
                "razon": "Cliente vigente en sistema",
                "puede_continuar": True,
                "mensaje": f"Cliente {cliente_data.get('nombre', 'N/A')} verificado como vigente."
            }

        return {
            "vigente": False,
            "estado": EstadoVigencia.NO_ENCONTRADO.value,
            "razon": "Cliente no encontrado en registros",
            "puede_continuar": False,
            "mensaje": "El cliente no fue encontrado en los registros de la empresa."
        }

    @staticmethod
    def obtener_resumen(resultado: Dict) -> Tuple[bool, str]:
        """Retorna si continuar y mensaje resumido"""
        return resultado["puede_continuar"], resultado["mensaje"]
