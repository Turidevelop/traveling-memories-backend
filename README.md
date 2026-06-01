# Traveling Memories Backend

> Una API REST moderna y completamente tipada para gestionar viajes y sus memorias, construida con FastAPI, SQLAlchemy y PostgreSQL.

## 📌 Descripción

**Traveling Memories Backend** es una aplicación web que proporciona una API REST para registrar, organizar y consultar información sobre viajes, lugares visitados y entradas de diario. Está diseñada siguiendo los principios de **Clean Architecture** para garantizar código mantenible, testeable y escalable.

### Características principales

- ✅ **API REST completamente funcional** con endpoints CRUD
- ✅ **Arquitectura limpia** con separación de capas (core, services, repositories, api)
- ✅ **Tipado estricto** en Python con type hints y Pydantic
- ✅ **Async/await** para operaciones no bloqueantes
- ✅ **Autenticación** mediante API Key
- ✅ **Base de datos PostgreSQL** con esquema bien estructurado
- ✅ **Tests automatizados** con pytest
- ✅ **Docker y Docker Compose** para despliegue
- ✅ **Gestión de entidades relacionadas**: Usuarios, Viajes, Ciudades, Países, Lugares Visitados, Entradas de Diario

---

## 📁 Estructura del proyecto

```
traveling-memories-backend/
├── docker-compose.yml           # Configuración de servicios (API + PostgreSQL)
├── Dockerfile                   # Imagen Docker de la aplicación
├── DOCKER.md                    # Guía detallada para despliegue con Docker
├── requirements.txt             # Dependencias de Python
├── .env.example                 # Template de variables de entorno
├── README.md                    # Este archivo
│
├── app/
│   ├── main.py                  # Punto de entrada de FastAPI
│   ├── database.py              # Configuración y sesiones async de SQLAlchemy
│   │
│   ├── core/                    # Capa de lógica de negocio central (framework-agnostic)
│   │   ├── config.py            # Configuración de la aplicación y variables de entorno
│   │   ├── models.py            # Modelos de dominio SQLAlchemy
│   │   ├── schemas.py           # Esquemas Pydantic para validación de requests/responses
│   │   └── security.py          # Funciones de seguridad (validación de API Key, etc.)
│   │
│   ├── repositories/            # Capa de acceso a datos (Data Access Layer)
│   │   ├── user_repo.py         # Repositorio de usuarios
│   │   ├── trip_repo.py         # Repositorio de viajes
│   │   ├── place_visited_repo.py# Repositorio de lugares visitados
│   │   ├── trip_entry_repo.py   # Repositorio de entradas de diario
│   │   ├── city_repo.py         # Repositorio de ciudades
│   │   └── country_repo.py      # Repositorio de países
│   │
│   ├── services/                # Capa de casos de uso (Use Case Layer)
│   │   ├── user_service.py      # Lógica de negocio de usuarios
│   │   ├── trip_service.py      # Lógica de negocio de viajes
│   │   ├── place_visited_service.py
│   │   ├── trip_entry_service.py
│   │   ├── city_service.py
│   │   └── country_service.py
│   │
│   ├── api/                     # Capa de presentación (API Layer)
│   │   ├── dependencies.py      # Inyección de dependencias
│   │   └── endpoints/           # Rutas REST
│   │       ├── user_endpoint.py
│   │       ├── trip_endpoint.py
│   │       ├── place_visited_endpoint.py
│   │       ├── trip_entry_endpoint.py
│   │       ├── city_endpoint.py
│   │       └── country_endpoint.py
│   │
│   └── __init__.py
│
├── test/                        # Pruebas automatizadas
│   ├── test_user_endpoint.py
│   ├── test_trip_endpoint.py
│   ├── test_place_visited_endpoint.py
│   ├── test_trip_entry_endpoint.py
│   ├── test_city_endpoint.py
│   ├── test_country_endpoint.py
│   └── __init__.py
│
└── DB/                          # Scripts SQL
    ├── create_roles_app.sql     # Creación de roles PostgreSQL
    ├── create_schema_travel_and_tables.sql  # Creación de esquema y tablas
    ├── insert_countries.sql     # Datos iniciales de países
    ├── insert_into_appuser.sql  # Datos iniciales de usuarios
    └── travel_db.session.sql    # Configuración de sesión
```

---

## 🛠️ Tecnologías

| Categoría | Herramientas |
|-----------|-------------|
| **Framework API** | [FastAPI](https://fastapi.tiangolo.com/) 0.115+ |
| **ORM & Database** | [SQLAlchemy](https://www.sqlalchemy.org/) 2.0+, [PostgreSQL](https://www.postgresql.org/) |
| **Async Driver** | [asyncpg](https://magicstack.github.io/asyncpg/) 0.30+ |
| **Validación** | [Pydantic](https://docs.pydantic.dev/) 2.11+, [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| **Testing** | [pytest](https://pytest.org/) 8.4+, [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio), [httpx](https://www.python-httpx.org/) |
| **Linting & Type Checking** | [mypy](https://www.mypy-lang.org/), [ruff](https://github.com/astral-sh/ruff) |
| **Utilities** | [python-dotenv](https://github.com/theskumar/python-dotenv), [uvicorn](https://www.uvicorn.org/) |
| **Database Driver** | [psycopg2](https://www.psycopg.org/) |

---

## 🏗️ Arquitectura

El proyecto sigue **Clean Architecture** con una separación clara de responsabilidades:

### Capas

```
┌─────────────────────────────────────────┐
│         API Layer (Presentation)        │
│  endpoints/ (FastAPI Routes + Schemas)  │
└──────────────────┬──────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│      Services Layer (Use Cases)          │
│   Business logic & workflows             │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│   Repositories Layer (Data Access)       │
│   Database queries & persistence         │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│    Core Layer (Domain & Config)          │
│  Models, schemas, configuration          │
└──────────────────────────────────────────┘
```

### Ventajas

- **Independencia de framework**: La lógica de negocio no depende de FastAPI
- **Testabilidad**: Fácil inyectar mocks en tests
- **Escalabilidad**: Agregar nuevas funcionalidades sin afectar código existente
- **Mantenibilidad**: Código organizado y con responsabilidades claras

---

## 🔑 Conceptos clave

### 1. **Type Hints & Pydantic**

Toda la aplicación usa type hints de Python. Los esquemas de entrada/salida se validan con Pydantic:

```python
# En schemas.py
class UserOut(BaseModel):
    id: int
    name: str
    avatar_url: str | None = None
    bio: str | None = None

# En endpoints
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, service: UserService = Depends()) -> UserOut:
    ...
```

### 2. **Async/Await**

Todas las operaciones de I/O (base de datos, API) son asincrónicas:

```python
async def get_all_users(self) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()
```

### 3. **Inyección de Dependencias**

FastAPI maneja automáticamente la inyección de dependencias:

```python
@router.get("/trips")
async def get_trips(
    service: TripService = Depends(),
    db: AsyncSession = Depends(get_db)
):
    ...
```

### 4. **Autenticación**

Se valida mediante API Key en los endpoints:

```python
@router.get("/users", dependencies=[Depends(validate_api_key)])
async def get_users(...):
    ...
```

---

## 🚀 Inicio rápido

### Requisitos previos

- Python 3.9+
- PostgreSQL 12+ (local o Neon)
- Docker & Docker Compose (opcional)

---

### Opción A: Con Docker Compose (Recomendado para desarrollo)

```bash
# Clonar repositorio
git clone <repository-url>
cd traveling-memories-backend

# Iniciar servicios (API + PostgreSQL)
docker-compose up -d

# La API estará disponible en http://localhost:8000/docs
```

---

### Opción B: Sin Docker (Local)

**1. Clonar y preparar el entorno**

```bash
# Clonar repositorio
git clone <repository-url>
cd traveling-memories-backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

**2. Configurar variables de entorno**

```bash
# Crear archivo .env basado en el template
cp .env.example .env

# Editar .env con tus valores de BD local
```

**3. Inicializar la base de datos**

```bash
# Ejecutar scripts SQL en PostgreSQL
psql -U postgres -f DB/00_init.sh
psql -U postgres -f DB/02_grant_permissions.sql
psql -U postgres -f DB/03_create_schema_travel_and_tables.sql
psql -U postgres -f DB/04_insert_countries.sql
psql -U postgres -f DB/05_insert_into_appuser.sql
```

**4. Ejecutar la aplicación**

```bash
# Desarrollo (con hot-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# La API estará disponible en http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

---

### Opción C: Producción (Render/Railway)

**Prerequisitos:**
- Cuenta en [Neon](https://neon.tech/) o [Supabase](https://supabase.com/) para BD PostgreSQL
- Cuenta en [Render](https://render.com/) o [Railway](https://railway.app/)

**Pasos:**

1. **Crear base de datos en Neon:**
   - Crear nuevo proyecto
   - Copiar `DATABASE_URL`
   - Ejecutar scripts SQL en la consola de Neon

2. **Conectar repositorio:**
   - Push código a GitHub (repo puede ser público)
   - En Render/Railway: conectar el repo

3. **Configurar variables de entorno:**
   - En el dashboard de Render/Railway, agregar:
     ```
     DATABASE_URL=postgresql+asyncpg://...
     ENVIRONMENT=production
     API_KEY=<generar-nueva-clave>
     DB_ADMIN_USER=administrador
     DB_ADMIN_PASSWORD=<contraseña>
     DB_APP_USER=app_user
     DB_APP_PASSWORD=<contraseña>
     ```

4. **Deploy automático:**
   - Render/Railway deploya automáticamente en cada push a main
   - Acceder vía URL pública proporcionada

**Generar nueva API_KEY:**
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)
```

---

## 🐳 Comandos Docker útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f app

# Ejecutar comando en el contenedor
docker-compose exec app bash

# Reconstruir imagen
docker-compose build

# Limpiar todo
docker-compose down -v
```

---

## 📚 Guía de uso de la API

### Autenticación

Todos los endpoints requieren el header `X-API-Key`:

```bash
curl -H "X-API-Key: tu-api-key" http://localhost:8000/users
```

### Ejemplos de endpoints

#### Viajes

```bash
# Listar viajes
GET /trips

# Obtener viaje por ID
GET /trips/{id}

# Crear viaje
POST /trips
Body: { "title": "Viaje a Europa", "start_date": "2024-01-01", "end_date": "2024-01-31", "user_id": 1, ... }
```

#### Ciudades y Países

```bash
# Listar países
GET /countries

# Listar ciudades
GET /cities

# Listar ciudades de un país
GET /cities?country_id=1
```

Para ver la documentación interactiva completa, accede a `/docs` en tu navegador.

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura de código
pytest --cov=app

# Tests de un módulo específico
pytest test/test_user_endpoint.py

# Con output detallado
pytest -v
```

---

## 🔧 Convenciones de código

### Naming

- **Servicios**: `*_service.py` (ej: `user_service.py`)
- **Repositorios**: `*_repo.py` (ej: `user_repo.py`)
- **Endpoints**: `*_endpoint.py` (ej: `user_endpoint.py`)

### Patrones

- **Modelos**: Se definen en `core/models.py` usando SQLAlchemy
- **Esquemas**: Se definen en `core/schemas.py` usando Pydantic
- **Rutas**: Se crean con `APIRouter` en `api/endpoints/`

### Type Hints

Siempre usa type hints. Ejemplos:

```python
def get_users() -> List[UserOut]:
    ...

async def create_user(user: UserCreate) -> UserOut:
    ...

def calculate_duration(start: date, end: date) -> int:
    ...
```

---

## 📊 Modelo de datos

### Entidades principales

```
User (Usuario)
├── id: int (PK)
├── name: str
├── avatar_url: str | null
└── bio: str | null

Trip (Viaje)
├── id: int (PK)
├── title: str
├── start_date: date
├── end_date: date
├── user_id: int (FK → User)
├── cover_photo_url: str | null
├── summary: str | null
└── created_at: timestamp

City (Ciudad)
├── id: int (PK)
├── name: str
├── lat: float
├── lng: float
└── country_id: int (FK → Country)

Country (País)
├── id: int (PK)
└── name: str (unique)

PlaceVisited (Lugar Visitado)
├── id: int (PK)
├── trip_id: int (FK → Trip)
├── country_id: int (FK → Country)
└── city_id: int (FK → City)

TripEntry (Entrada de Diario)
├── id: int (PK)
├── trip_id: int (FK → Trip)
├── entry_date: date
├── title: str
└── content: text
```

---

## 🛠️ Variables de entorno

Ver `.env.example` para todas las variables disponibles.

**Variables requeridas:**

```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/name_db

# Credenciales de BD (para inicialización)
DB_ADMIN_USER=administrador
DB_ADMIN_PASSWORD=contraseña-admin
DB_APP_USER=app_user
DB_APP_PASSWORD=contraseña-app

# Configuración
ENVIRONMENT=development          # development | production
API_KEY=tu-clave-secreta-aqui   # Generar con: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Importante:** Nunca subir `.env` al repositorio. Usar `.env.example` como referencia.

---

## 📖 Recursos útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [asyncpg](https://magicstack.github.io/asyncpg/)
- [pytest Documentation](https://docs.pytest.org/)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
2. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
3. Push a la rama (`git push origin feature/AmazingFeature`)
4. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver LICENSE para más detalles.

---

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Última actualización**: Febrero 2026  
**Versión**: 1.0.0

---

