import random
import string
from models import ResultadoMetaSimulado


class MetaSimulator:
    """Simulador de búsqueda en Meta (Instagram/Facebook)

    NOTA MVP: Esto es una simulación para demostración.
    En producción, se integraría con Meta Ads API real.
    """

    # Perfiles predefinidos para emails específicos (datos de prueba)
    PERFILES_ESPECIALES = {
        "jairfabian93@gmail.com": {
            "usuario_instagram": "@jair.fabian.93",
            "usuario_facebook": "jair.fabian.93",
            "seguidores": 2850,
            "ciudad": "Bogota",
            "perfil_url": "https://www.instagram.com/jair.fabian.93/"
        },
        "maria.rodriguez@email.com": {
            "usuario_instagram": "@maria.rodriguez_",
            "usuario_facebook": "maria.rodriguez.oficina",
            "seguidores": 1240,
            "ciudad": "Medellin",
            "perfil_url": "https://www.instagram.com/maria.rodriguez_/"
        }
    }

    @staticmethod
    def generar_usuario_instagram(nombre: str) -> str:
        """Genera un nombre de usuario Instagram ficticio basado en el nombre"""
        base = nombre.lower().replace(" ", "").replace("á", "a").replace("é", "e")
        numeros = "".join(random.choices(string.digits, k=random.randint(2, 4)))
        return f"{base}{numeros}"

    @staticmethod
    def generar_usuario_facebook(nombre: str) -> str:
        """Genera un nombre de usuario Facebook ficticio"""
        base = nombre.lower().replace(" ", ".")
        return f"{base}.skandia{random.randint(1000, 9999)}"

    @staticmethod
    def buscar_cliente_en_meta(email: str, cliente_data: dict = None) -> ResultadoMetaSimulado:
        """Simula búsqueda de cliente en Meta por email

        En el MVP, siempre encuentra al cliente si existe en la BD.
        En producción, usaría Custom Audiences API de Meta.
        """

        if not cliente_data:
            return ResultadoMetaSimulado(
                encontrado=False,
                email=email,
                usuario_instagram=None,
                usuario_facebook=None,
                seguidores=None,
                ciudad_red_social=None,
                perfil_url=None
            )

        # Verificar si hay perfil predefinido para este email
        email_lower = email.lower()
        if email_lower in MetaSimulator.PERFILES_ESPECIALES:
            perfil = MetaSimulator.PERFILES_ESPECIALES[email_lower]
            return ResultadoMetaSimulado(
                encontrado=True,
                email=email,
                usuario_instagram=perfil["usuario_instagram"],
                usuario_facebook=perfil["usuario_facebook"],
                seguidores=perfil["seguidores"],
                ciudad_red_social=perfil["ciudad"],
                perfil_url=perfil["perfil_url"]
            )

        # Simulamos que encontramos al cliente en Meta (generado aleatoriamente)
        nombre = cliente_data.get("nombre", "Usuario")
        ciudad = cliente_data.get("ciudad", "Bogota")

        ig_user = MetaSimulator.generar_usuario_instagram(nombre)
        fb_user = MetaSimulator.generar_usuario_facebook(nombre)
        seguidores = random.randint(50, 5000)

        return ResultadoMetaSimulado(
            encontrado=True,
            email=email,
            usuario_instagram=f"@{ig_user}",
            usuario_facebook=fb_user,
            seguidores=seguidores,
            ciudad_red_social=ciudad,
            perfil_url=f"https://instagram.com/{ig_user}/"  # Ficticio
        )

    @staticmethod
    def generar_mensaje_publicidad(cliente_data: dict) -> str:
        """Genera mensaje de publicidad personalizado para el cliente"""
        nombre = cliente_data.get("nombre", "Cliente")
        ciudad = cliente_data.get("ciudad", "tu ciudad")

        mensajes = [
            f"¡Hola {nombre}! 👋 Notamos que tu perfil en nuestro sistema tiene información desactualizada. Actualiza tus datos para recibir ofertas personalizadas 🎁",
            f"Hola {nombre}, ¿vivís en {ciudad}? Verifica tu información con Skandia para acceso a mejores beneficios 💼",
            f"{nombre}, es hora de actualizar tu perfil en Skandia. ¡Nuevas opciones te esperan! 🚀",
        ]
        return random.choice(mensajes)
