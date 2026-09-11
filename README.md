# 🎯 Skandia Meta Simulator MVP

MVP para localizar clientes en redes sociales (Meta: Instagram/Facebook) y promover actualización de datos personales.

## 🚀 Características

- **Simulador de búsqueda en Meta**: Busca clientes por email y simula encontrarlos en Instagram/Facebook
- **Generación de publicidad contextual**: Crea mensajes publicitarios personalizados basados en datos del cliente
- **Sistema de actualización de datos**: Formulario web donde clientes actualizan su información
- **Dashboard**: Vista general de clientes que requieren actualización
- **Integración Cosmos DB**: Persistencia en Azure Cosmos DB

## 📋 Stack Técnico

- **Backend**: Python 3.11+ + FastAPI
- **Base de datos**: Azure Cosmos DB (SQL/Core API)
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Credenciales**: python-dotenv (.env)

## ⚙️ Instalación y Setup

### 1. Clonar/Preparar el proyecto

```bash
cd C:\Users\jtamara\Documents\Hackaton
```

### 2. Crear archivo `.env`

Copia `.env.example` a `.env` y completa con tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con:
```
COSMOS_URL=https://<tu-cosmos-account>.documents.azure.com:443/
COSMOS_KEY=<tu-cosmos-primary-key>
COSMOS_DATABASE=skandia_hackathon
COSMOS_CONTAINER=clientes
APP_HOST=localhost
APP_PORT=8000
```

**¿Cómo obtener credenciales de Cosmos DB?**
1. Azure Portal → Cosmos DB Account
2. Settings → Keys
3. Copia: `URI` (COSMOS_URL) y `Primary Key` (COSMOS_KEY)

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar setup (crear BD y datos de prueba)

```bash
python setup_cosmos.py
```

**Output esperado:**
```
============================================================
SETUP: SKANDIA HACKATHON - META SIMULATOR
============================================================

📡 Conectando a Cosmos DB...

📦 Creando base de datos y contenedor...
✓ Base de datos 'skandia_hackathon' lista
✓ Contenedor 'clientes' listo

👥 Insertando clientes de prueba...

  • Carlos García López         | carlos.garcia@email.com
    ✓ Actualizado

  • María Rodríguez Pérez       | maria.rodriguez@email.com
    ⚠️  REQUIERE ACTUALIZACIÓN

  • Juan Pablo Martínez         | juan.martinez@email.com
    ✓ Actualizado

============================================================
✅ Setup completado exitosamente
============================================================

📝 PRÓXIMOS PASOS:
  1. Instala dependencias:  pip install -r requirements.txt
  2. Inicia el servidor:    python app.py
  3. Abre en navegador:     http://localhost:8000

🧪 USUARIO DE PRUEBA para ver simulación de Meta:
  Email: maria.rodriguez@email.com
  (Este cliente tiene requiere_actualizacion=True)
```

### 5. Iniciar servidor

```bash
python app.py
```

**Output esperado:**
```
============================================================
🚀 SKANDIA META SIMULATOR - FastAPI Server
============================================================
🌐 Servidor iniciando en: http://localhost:8000
📚 Documentación API: http://localhost:8000/docs
============================================================
```

## 🧪 Flujo de Prueba

### Escenario 1: Cliente que Requiere Actualización

1. Abre http://localhost:8000
2. En tab **"🔍 Buscar Cliente"**, ingresa: `maria.rodriguez@email.com`
3. Verás:
   - ✅ Datos personales del cliente
   - ⚠️ Estado: "REQUIERE ACTUALIZACIÓN"
   - 📢 Mensaje publicitario personalizado
   - 🔎 Simulación de búsqueda en Meta (Instagram/Facebook con usuario ficticio)
   - 📝 Botón "Actualizar Datos"

4. Haz clic en "📝 Actualizar Datos"
5. Actualiza campos (nombre, teléfono, ciudad)
6. Haz clic en "💾 Guardar Cambios"
7. Verás: "✅ Datos actualizados correctamente"
8. El cliente vuelve al estado "Actualizado"

### Escenario 2: Ver Dashboard

1. En tab **"📊 Dashboard"**:
   - Total de clientes actualizados
   - Total que requieren actualización
   - Lista interactiva de clientes
2. Puedes hacer clic en un cliente para buscarlo directamente

## 📁 Estructura del Proyecto

```
hackathon-skandia/
├── .env.example                  # Template de variables de entorno
├── .env                           # Variables de entorno (NO COMMITTEAR)
├── requirements.txt               # Dependencias Python
├── README.md                      # Este archivo
│
├── cosmos_client.py               # Cliente Cosmos DB
├── models.py                      # Modelos Pydantic
├── meta_simulator.py              # Simulador de búsqueda Meta
├── setup_cosmos.py                # Script de setup inicial
├── app.py                         # Aplicación FastAPI (main)
│
└── static/
    ├── index.html                 # Dashboard principal
    ├── formulario_actualizacion.html  # Formulario de actualización
```

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Dashboard principal |
| GET | `/formulario/{email}` | Formulario de actualización |
| GET | `/api/cliente/buscar?email=...` | Busca cliente + simula Meta |
| POST | `/api/cliente/{email}/actualizar` | Actualiza datos del cliente |
| GET | `/api/clientes/todos` | Lista todos los clientes |
| GET | `/api/clientes/requieren-actualizacion` | Lista clientes con actualización pendiente |
| GET | `/api/health` | Health check |

**Docs interactiva:** http://localhost:8000/docs (Swagger UI)

## 📝 Notas Importantes

### MVP vs Producción

| Aspecto | MVP | Producción |
|--------|-----|-----------|
| **Búsqueda Meta** | Simulada (genera usuarios ficticios) | Meta Ads API + Custom Audiences |
| **Detección de actualización** | Manual (campos en BD) | Webhooks de rebotes de email, cambios de ubicación, etc. |
| **Autenticación** | Sin autenticación | OAuth2 + B2C de Skandia |
| **Envío publicitario** | Simulado en formulario | Meta Ads API + campañas reales |
| **Logs/Auditoría** | Print en console | CyberLog + Application Insights |

### Considerar para Producción

- ✅ Integración real con **Meta Ads API** (Custom Audiences, Conversions API)
- ✅ Sistema de **detección automática** de datos desactualizados (rebotes de email, geolocalización)
- ✅ **Autenticación** con Azure B2C
- ✅ **Rate limiting** y throttling
- ✅ **Auditoría** de cambios (quién, cuándo, qué cambió)
- ✅ **Consentimiento** de marketing (GDPR compliance)
- ✅ **Logging centralizado** (Application Insights)
- ✅ **Retry logic** para fallos de Cosmos
- ✅ Tests unitarios y de integración
- ✅ CI/CD pipeline (GitHub Actions/Azure DevOps)

## 🐛 Troubleshooting

### Error: "COSMOS_URL and COSMOS_KEY not configured"

**Solución:** Verifica que `.env` existe y tiene las credenciales correctas.

```bash
cat .env
```

### Error: "Connection refused" al conectar a Cosmos

**Solución:** 
1. Verifica que `COSMOS_URL` es correcto (sin espacios)
2. Verifica que `COSMOS_KEY` es la clave primaria (no secundaria)
3. Comprueba firewall/red

### Puerto 8000 ya en uso

**Solución:** Cambia el puerto en `.env`:

```
APP_PORT=8001
```

### Clientes no aparecen después de setup

**Solución:**
1. Verifica que `setup_cosmos.py` corrió sin errores
2. Abre Azure Portal → Cosmos DB → Data Explorer
3. Verifica que exista DB `skandia_hackathon` y contenedor `clientes`

## 📚 Recursos Útiles

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Azure Cosmos DB Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-db)
- [Meta Ads API](https://developers.facebook.com/docs/marketing-apis)
- [python-dotenv](https://python-dotenv.readthedocs.io/)

## 👨‍💻 Autor

MVP desarrollado para Hackathon Skandia 2026

## 📄 Licencia

Uso interno Skandia - Todos los derechos reservados
