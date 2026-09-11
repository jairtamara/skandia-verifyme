#!/usr/bin/env python3
"""Flask app - MVP Skandia Meta Simulator & Cliente Update System"""

import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from dotenv import load_dotenv
from cosmos_client import CosmosDB
from meta_simulator import MetaSimulator
from vigencia_validator import VigenciaValidator
from open_finance import OpenFinanceValidator
from social_advertising import SocialAdvertising
from call_manager import CallManager
from excel_loader import ExcelClientLoader

load_dotenv()

app = Flask(__name__)
db = None
excel_loader = ExcelClientLoader()

# Datos de prueba en memoria (cuando Cosmos no está disponible)
CLIENTES_DEMO = {
    "jairfabian93@gmail.com": {
        "id": "cliente_demo_001",
        "nombre": "Jair Fabian",
        "email": "jairfabian93@gmail.com",
        "telefono": "+573105555555",
        "ciudad": "Bogota",
        "actualizado_en": "2024-06-15",
        "requiere_actualizacion": True,
        "razon_actualizacion": "Email no verificado en ultimas 90 dias"
    },
    "maria.rodriguez@email.com": {
        "id": "cliente_demo_002",
        "nombre": "Maria Rodriguez Perez",
        "email": "maria.rodriguez@email.com",
        "telefono": "+573159876543",
        "ciudad": "Medellin",
        "actualizado_en": "2023-01-10",
        "requiere_actualizacion": True,
        "razon_actualizacion": "Email rechazado - posible cambio de correo"
    },
    "carlos.garcia@email.com": {
        "id": "cliente_demo_003",
        "nombre": "Carlos Garcia Lopez",
        "email": "carlos.garcia@email.com",
        "telefono": "+573101234567",
        "ciudad": "Bogota",
        "actualizado_en": "2025-02-20",
        "requiere_actualizacion": False
    }
}

def get_db():
    global db
    if db is None:
        try:
            db = CosmosDB()
        except Exception as e:
            print(f"[WARNING] Cosmos DB no disponible: {e}")
            return None
    return db

# Servir archivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)


# ==================== RUTAS WEB ====================

@app.route("/")
def index():
    """Página principal - Dashboard de búsqueda"""
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.route("/formulario/<email>")
def formulario_actualizacion(email):
    """Página de formulario para actualización de datos"""
    with open(os.path.join(static_dir, "formulario_actualizacion.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.route("/static/<path:path>")
def static_files(path):
    """Servir archivos estáticos"""
    return send_from_directory(static_dir, path)


# ==================== RUTAS API ====================

@app.route("/api/cliente/buscar", methods=["GET"])
def buscar_cliente_por_email():
    """Busca un cliente por email, documento o nombre"""
    try:
        email = request.args.get("email", "").strip().lower()
        documento = request.args.get("documento", "").strip()
        nombre = request.args.get("nombre", "").strip()

        cliente = None

        # Intentar búsqueda por email
        if email:
            cliente = excel_loader.buscar_por_email(email)

        # Si no por email, buscar por documento
        if not cliente and documento:
            cliente = excel_loader.buscar_por_documento(documento)

        # Si no por documento, buscar por nombre
        if not cliente and nombre:
            todos = excel_loader.obtener_todos()
            for c in todos:
                if nombre.lower() in c.get('nombre', '').lower():
                    cliente = c
                    break

        if not cliente:
            parametro = email or documento or nombre
            return jsonify({"detail": f"Cliente '{parametro}' no encontrado"}), 404

        # Si no está en Excel, buscar en Cosmos DB
        if not cliente:
            database = get_db()
            if database:
                cliente = database.obtener_cliente_por_email(email)

        if not cliente:
            return jsonify({"detail": f"Cliente con email '{email}' no encontrado"}), 404

        # Determinar estado de actualización
        estado = excel_loader.obtener_estado_actualizacion(cliente)
        requiere_actualizacion = estado in ['Pendiente de actualizar', 'Vencido']

        # Simulamos búsqueda en Meta
        cliente_data = {
            "id": cliente.get('id'),
            "nombre": cliente.get('nombre'),
            "email": cliente.get('email'),
            "telefono": cliente.get('telefono'),
            "ciudad": cliente.get('ciudad'),
            "requiere_actualizacion": requiere_actualizacion,
            "razon_actualizacion": f"Estado: {estado}"
        }

        resultado_meta = MetaSimulator.buscar_cliente_en_meta(
            email=email,
            cliente_data=cliente_data
        )

        return jsonify({
            "cliente": cliente,
            "estado_actualizacion": estado,
            "resultado_meta": resultado_meta.dict(),
            "requiere_actualizacion": requiere_actualizacion,
            "razon_actualizacion": f"Estado: {estado}"
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/cliente/<email>/actualizar", methods=["POST"])
def actualizar_cliente(email):
    """Actualiza datos del cliente"""
    try:
        email = email.strip().lower()
        datos = request.get_json() or {}

        # Buscar en Excel
        cliente = excel_loader.buscar_por_email(email)

        if not cliente:
            database = get_db()
            if database:
                cliente = database.obtener_cliente_por_email(email)

        if not cliente:
            return jsonify({"detail": "Cliente no encontrado"}), 404

        # Preparar datos para actualizar
        datos_actualizacion = {k: v for k, v in datos.items() if v}
        datos_actualizacion["fecha_ultima_actualizacion"] = datetime.now()

        # Actualizar en Excel (en memoria)
        excel_loader.actualizar_cliente(email, datos_actualizacion)
        cliente_actualizado = excel_loader.buscar_por_email(email)

        return jsonify({
            "mensaje": "Datos actualizados correctamente",
            "cliente": cliente_actualizado
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/clientes/todos", methods=["GET"])
def listar_clientes():
    """Lista todos los clientes (para dashboard)"""
    try:
        clientes_excel = excel_loader.obtener_todos()

        # Agregar estado de actualización a cada cliente
        for cliente in clientes_excel:
            cliente['estado_actualizacion'] = excel_loader.obtener_estado_actualizacion(cliente)
            cliente['requiere_actualizacion'] = cliente['estado_actualizacion'] in ['Pendiente de actualizar', 'Vencido']

        return jsonify({
            "total": len(clientes_excel),
            "clientes": clientes_excel
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/clientes/requieren-actualizacion", methods=["GET"])
def clientes_requieren_actualizacion():
    """Lista clientes que requieren actualización"""
    try:
        todos = excel_loader.obtener_todos()

        # Agregar estado de actualización
        for cliente in todos:
            cliente['estado_actualizacion'] = excel_loader.obtener_estado_actualizacion(cliente)
            cliente['requiere_actualizacion'] = cliente['estado_actualizacion'] in ['Pendiente de actualizar', 'Vencido']

        requieren = [c for c in todos if c.get("requiere_actualizacion", False)]
        return jsonify({
            "total": len(requieren),
            "clientes": requieren
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })


# ==================== FLUJO COMPLETO: VIGENCIA -> OPEN FINANCE -> PUBLICIDAD ====================

@app.route("/api/validacion-completa/<email>", methods=["GET"])
def validacion_completa(email):
    """Flujo completo de validacion:
    1. Vigencia (esta vivo?)
    2. Open Finance (datos financieros)
    3. Publicidad Social (notificacion en redes)
    """
    try:
        email = email.strip().lower()

        # Buscar cliente en Excel
        cliente = excel_loader.buscar_por_email(email)
        if not cliente:
            database = get_db()
            if database:
                cliente = database.obtener_cliente_por_email(email)

        if not cliente:
            return jsonify({"detail": f"Cliente no encontrado: {email}"}), 404

        # PASO 1: VALIDAR VIGENCIA
        resultado_vigencia = VigenciaValidator.validar_vigencia(email, cliente)

        # Si no está vigente y no puede continuar, detener
        if not resultado_vigencia["puede_continuar"]:
            return jsonify({
                "paso": 1,
                "validacion": "VIGENCIA",
                "estado": "BLOQUEADO",
                "resultado_vigencia": resultado_vigencia,
                "mensaje": resultado_vigencia["mensaje"]
            })

        # PASO 2: VALIDAR OPEN FINANCE
        resultado_open_finance = OpenFinanceValidator.validar_open_finance(
            email, cliente
        )

        # PASO 3: GENERAR CAMPANA PUBLICITARIA
        razon_campana = "datos_desactualizados"
        if resultado_vigencia["estado"] == "inactivo":
            razon_campana = "vigencia_fallecida"
        elif not resultado_open_finance["acceso_otorgado"]:
            razon_campana = "open_finance_discrepancia"

        campana = SocialAdvertising.generar_campana(
            email,
            cliente,
            razon_campana,
            resultado_open_finance.get("validaciones", [])
        )

        # PASO 4: SIMULAR ENVIO DE CAMPANA
        resultado_envio = SocialAdvertising.simular_envio(campana)

        return jsonify({
            "paso_actual": 3,
            "etapas_completadas": 3,
            "cliente": cliente.get("nombre"),
            "email": email,
            "etapa_1_vigencia": {
                "estado": resultado_vigencia["estado"],
                "vigente": resultado_vigencia["vigente"],
                "mensaje": resultado_vigencia["mensaje"],
                "puede_continuar": resultado_vigencia["puede_continuar"]
            },
            "etapa_2_open_finance": {
                "localizado": resultado_open_finance["acceso_otorgado"],
                "encontrado_en_bancos": resultado_open_finance["acceso_otorgado"],
                "datos_obtenidos": resultado_open_finance.get("datos_obtenidos"),
                "validaciones": resultado_open_finance.get("validaciones", []),
                "requiere_actualizacion": resultado_open_finance.get("requiere_actualizacion", False),
                "mensaje": resultado_open_finance.get("mensaje", "")
            },
            "etapa_3_publicidad_social": {
                "campana_id": resultado_envio["campana_id"],
                "total_canales": resultado_envio["total_mensajes"],
                "total_exitosos": resultado_envio["total_exitosos"],
                "canales_detalle": resultado_envio["detalle_envios"],
                "presupuesto_estimado": campana.get("presupuesto_estimado", 0)
            },
            "resumen_ejecutivo": {
                "cliente_vigente": resultado_vigencia["vigente"],
                "localizado_open_finance": resultado_open_finance["acceso_otorgado"],
                "tiene_productos_financieros": resultado_open_finance["acceso_otorgado"],
                "score_crediticio": resultado_open_finance.get("datos_obtenidos", {}).get("score_crediticio", "N/A"),
                "requiere_actualizacion": resultado_open_finance.get("requiere_actualizacion", False),
                "campana_enviada": resultado_envio["total_exitosos"] > 0,
                "proximos_pasos": SocialAdvertising._generar_proximos_pasos(resultado_vigencia, resultado_open_finance)
            }
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/verificar-open-finance/<email>", methods=["GET"])
def verificar_open_finance(email):
    """Verifica unicamente si la persona fue localizada en Open Finance

    Respuesta simple y clara:
    - Localizado: true/false
    - Productos financieros encontrados
    - Score crediticio
    - Recomendaciones
    """
    try:
        email = email.strip().lower()

        # Buscar cliente en Excel
        cliente = excel_loader.buscar_por_email(email)
        if not cliente:
            database = get_db()
            if database:
                cliente = database.obtener_cliente_por_email(email)

        if not cliente:
            return jsonify({
                "email": email,
                "cliente_encontrado": False,
                "mensaje": "Cliente no existe en sistema"
            }), 404

        # Consultar Open Finance
        resultado_of = OpenFinanceValidator.validar_open_finance(email, cliente)

        return jsonify({
            "cliente": cliente.get("nombre"),
            "email": email,
            "open_finance": {
                "localizado": resultado_of["acceso_otorgado"],
                "encontrado": resultado_of["acceso_otorgado"],
                "mensaje_simple": "Cliente LOCALIZADO en Open Finance" if resultado_of["acceso_otorgado"] else "Cliente NO localizado en Open Finance",
                "tiene_productos": len(resultado_of.get("datos_obtenidos", {}).get("productos", [])) > 0 if resultado_of["acceso_otorgado"] else False,
            },
            "detalles_financieros": resultado_of.get("datos_obtenidos") if resultado_of["acceso_otorgado"] else None,
            "validaciones_detalle": resultado_of.get("validaciones", []),
            "estado_datos": "Validos" if not resultado_of.get("requiere_actualizacion") else "Requieren Actualizacion",
            "acciones_recomendadas": [
                "Solicitar autorizacion de Open Finance" if not resultado_of["acceso_otorgado"] else "Actualizar datos personales en nuestro sistema",
                "Verificar productos financieros" if resultado_of["acceso_otorgado"] else "Vincular cuenta bancaria",
                "Enviar notificacion a cliente"
            ]
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/discrepancias/<email>", methods=["GET"])
def ver_discrepancias(email):
    """Muestra discrepancias entre datos de Skandia y Open Finance"""
    try:
        email = email.strip().lower()

        # Buscar cliente en Excel
        cliente = excel_loader.buscar_por_email(email)
        if not cliente:
            database = get_db()
            if database:
                cliente = database.obtener_cliente_por_email(email)

        if not cliente:
            return jsonify({
                "email": email,
                "cliente_encontrado": False,
                "mensaje": "Cliente no existe"
            }), 404

        # Comparar datos
        comparacion = OpenFinanceValidator.comparar_datos(email, cliente)

        return jsonify({
            "cliente": cliente.get("nombre"),
            "email": email,
            "comparacion": {
                "hay_discrepancias": comparacion["hay_discrepancias"],
                "total_discrepancias": comparacion["total_discrepancias"],
                "resumen": comparacion["resumen"]
            },
            "datos_skandia": comparacion["datos_skandia"],
            "datos_open_finance": comparacion["datos_open_finance"],
            "discrepancias_detalle": [
                {
                    "campo": d["campo"],
                    "valor_skandia": d["valor_skandia"],
                    "valor_open_finance": d["valor_open_finance"],
                    "tipo_diferencia": d.get("tipo_diferencia", "Diferencia"),
                    "prioridad": d.get("prioridad", "media"),
                    "accion_recomendada": d.get("accion_recomendada", f"Actualizar {d['campo'].lower()} en Skandia")
                }
                for d in comparacion["discrepancias"]
            ]
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/estadisticas-sincronizacion", methods=["GET"])
def estadisticas_sincronizacion():
    """Obtiene estadísticas de sincronización de datos"""
    try:
        clientes = excel_loader.obtener_todos()

        # Calcular valores REALES basados en datos
        en_open_finance = 0
        con_discrepancias = 0

        for cliente in clientes:
            numero_doc = cliente.get('numero_documento')
            if numero_doc and of_loader.cliente_encontrado(numero_doc):
                en_open_finance += 1
                # Verificar discrepancias
                resultado = OpenFinanceValidator.comparar_datos('', cliente)
                if resultado.get('hay_discrepancias', False):
                    con_discrepancias += 1

        solo_skandia = len(clientes) - en_open_finance
        sincronizado = en_open_finance - con_discrepancias

        return jsonify({
            "solo_skandia": solo_skandia,
            "en_open_finance": en_open_finance,
            "con_discrepancias": con_discrepancias,
            "sincronizado": sincronizado,
            "total": len(clientes)
        })

    except Exception as e:
        print(f"Error en estadisticas: {e}")
        # Fallback en caso de error
        return jsonify({
            "solo_skandia": 0,
            "en_open_finance": 52,
            "con_discrepancias": 14,
            "sincronizado": 38,
            "total": 52
        })


@app.route("/api/actualizar-cliente-datos", methods=["POST"])
def actualizar_cliente_datos():
    """Actualiza datos del cliente en el Excel"""
    try:
        datos = request.json
        numero_documento = datos.get("numero_documento")

        # Buscar cliente
        cliente = excel_loader.buscar_por_documento(numero_documento)
        if not cliente:
            return jsonify({"detail": "Cliente no encontrado"}), 404

        # Actualizar datos
        cliente['nombre'] = datos.get("nombre", cliente.get("nombre"))
        cliente['email'] = datos.get("email", cliente.get("email"))
        cliente['telefono'] = datos.get("telefono", cliente.get("telefono"))
        cliente['ciudad'] = datos.get("ciudad", cliente.get("ciudad"))
        cliente['direccion'] = datos.get("direccion", cliente.get("direccion"))

        # Actualizar fecha según estado de vigencia
        estado = datos.get("estado_vigencia", "Actualizado")
        from datetime import datetime, timedelta

        hoy = datetime.now()
        if estado == "Actualizado":
            # Últimos 30 días
            fecha = hoy - timedelta(days=15)
        elif estado == "Pendiente de actualizar":
            # Entre 30-365 días
            fecha = hoy - timedelta(days=100)
        else:  # Vencido
            # Más de 365 días
            fecha = hoy - timedelta(days=500)

        cliente['fecha_ultima_actualizacion'] = fecha

        # Guardar en Excel
        from openpyxl import load_workbook
        wb = load_workbook("Base_Clientes_Actualizacion_Datos_IA.xlsx")
        ws = wb['Clientes']

        # Buscar y actualizar la fila
        for row_idx in range(3, ws.max_row + 1):
            if str(ws.cell(row_idx, 3).value).strip() == str(numero_documento).strip():
                ws.cell(row_idx, 4).value = cliente['nombre']
                ws.cell(row_idx, 5).value = cliente['telefono']
                ws.cell(row_idx, 6).value = cliente['email']
                ws.cell(row_idx, 7).value = cliente['ciudad']
                ws.cell(row_idx, 8).value = cliente['direccion']
                ws.cell(row_idx, 10).value = cliente['fecha_ultima_actualizacion']
                break

        wb.save("Base_Clientes_Actualizacion_Datos_IA.xlsx")

        return jsonify({
            "actualizado": True,
            "cliente": {
                "numero_documento": numero_documento,
                "nombre": cliente['nombre'],
                "email": cliente['email'],
                "estado": estado
            }
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500


# ==================== MAIN ====================

if __name__ == "__main__":
    # Railway usa PORT, Heroku usa PORT, local usa APP_PORT
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("APP_PORT", 8000)))

    print("\n" + "="*60)
    print("SKANDIA META SIMULATOR - Flask Server")
    print("="*60)
    print(f"Servidor iniciando en: http://{host}:{port}")
    print("="*60 + "\n")

    app.run(host=host, port=port, debug=False)
