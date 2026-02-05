# Docker Setup Guide

> Guía completa para ejecutar Traveling Memories Backend en contenedores Docker con PostgreSQL.

---

## 📋 Requisitos previos

- **Docker** 20.10+
- **Docker Compose** 1.29+

### Verificar instalación

```bash
docker --version
docker-compose --version
```

---

## 🔐 Configuración de variables de entorno

### 1. Crear archivo `.env`

```bash
cp .env.example .env
```

### 2. Configurar variables

```env
# ============================================
# BASE DE DATOS - PostgreSQL Configuration
# ============================================
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=travel_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/travel_db

# ============================================
# API - FastAPI Configuration
# ============================================
API_KEY=tu-clave-secreta-muy-segura-aqui
ENVIRONMENT=development              # development | production | staging

# ============================================
# OPCIONAL - Logging and Debug
# ============================================
# LOG_LEVEL=info
# DEBUG=false
```

**Notas importantes:**
- En producción, cambia `DB_PASSWORD` a una contraseña fuerte
- Usa una `API_KEY` aleatoria y segura (genera con `openssl rand -hex 32`)
- Nunca commits el `.env` a Git (está en `.gitignore`)

---

## 🚀 Inicio rápido con Docker Compose

### Opción 1: Modo desarrollo (recomendado)

```bash
# Construir e iniciar todos los servicios
docker-compose up -d

# Ver el estado de los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api
docker-compose logs -f postgres
```

**Lo que se inicia:**
- ✅ PostgreSQL en `localhost:5432`
- ✅ FastAPI en `localhost:8000`
- ✅ Hot-reload activado para desarrollo

### Opción 2: Modo foreground (ver logs directamente)

```bash
# Sin -d, los logs aparecen en la terminal
docker-compose up
```

Presiona `Ctrl+C` para detener.

### Detener servicios

```bash
# Detener pero mantener datos
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores y volúmenes (⚠️ elimina datos)
docker-compose down -v
```

---

## 🔧 Operaciones comunes

### Ejecutar comandos en contenedores

```bash
# Acceder a la terminal del contenedor API
docker-compose exec api sh

# Ejecutar Python en el contenedor API
docker-compose exec api python -c "import sys; print(sys.version)"

# Acceder a PostgreSQL desde el contenedor
docker-compose exec postgres psql -U postgres -d travel_db
```

### Ver estado y logs

```bash
# Estado de servicios
docker-compose ps

# Inspeccionar un servicio
docker-compose exec api uvicorn --version

# Ver logs con timestamp
docker-compose logs --timestamps

# Últimas 50 líneas de logs
docker-compose logs -n 50 api

# Logs en tiempo real (sigue nuevos logs)
docker-compose logs -f api
```

### Reiniciar servicios

```bash
# Reiniciar un servicio específico
docker-compose restart api
docker-compose restart postgres

# Reiniciar todos
docker-compose restart

# Rebuild y reiniciar
docker-compose up -d --build
```

---

## 🐘 Gestión de PostgreSQL

### Conectarse a la base de datos

```bash
# Desde dentro del contenedor
docker-compose exec postgres psql -U postgres -d travel_db

# O con una herramienta externa (DBeaver, pgAdmin, etc.)
# Connection: localhost:5432
# User: postgres
# Password: postgres (o la que configuraste)
# Database: travel_db
```

### Ejecutar scripts SQL

```bash
# Desde el host
docker-compose exec postgres psql -U postgres -d travel_db < DB/insert_countries.sql

# Dentro del contenedor
docker-compose exec postgres bash
psql -U postgres -d travel_db -f /docker-entrypoint-initdb.d/insert_countries.sql
```

### Respaldar base de datos

```bash
# Crear dump
docker-compose exec postgres pg_dump -U postgres travel_db > backup.sql

# Restaurar desde dump
docker-compose exec -T postgres psql -U postgres travel_db < backup.sql
```

---

## 📡 Acceso a la API

| Servicio | URL |
|----------|-----|
| **API REST** | http://localhost:8000 |
| **Swagger UI (Docs)** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **OpenAPI JSON** | http://localhost:8000/openapi.json |

### Ejemplo de request

```bash
# Con curl
curl -H "X-API-Key: tu-api-key" http://localhost:8000/users

# Con httpx o requests en Python
python -c "
import httpx
headers = {'X-API-Key': 'tu-api-key'}
response = httpx.get('http://localhost:8000/users', headers=headers)
print(response.json())
"
```

---

## 🐳 Construcción manual (sin Compose)

### Build de la imagen

```bash
# Construir imagen con tag
docker build -t traveling-memories-api:1.0 .

# Construir sin cache
docker build --no-cache -t traveling-memories-api:latest .

# Listar imágenes
docker images | grep traveling
```

### Ejecutar contenedor manualmente

```bash
# Run básico (requiere PostgreSQL corriendo externamente)
docker run -d \
  --name traveling-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:password@db-host:5432/travel_db \
  -e API_KEY=tu-api-key \
  traveling-memories-api:latest

# Run con red personalizada
docker network create travel-net

docker run -d \
  --name postgres \
  --network travel-net \
  -e POSTGRES_PASSWORD=password \
  postgres:16-alpine

docker run -d \
  --name api \
  --network travel-net \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/travel_db \
  traveling-memories-api:latest
```

### Gestión de contenedores

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Logs de un contenedor
docker logs traveling-api

# Logs en tiempo real
docker logs -f traveling-api

# Ejecutar comando en contenedor
docker exec traveling-api python --version

# Detener contenedor
docker stop traveling-api

# Reanudar contenedor
docker start traveling-api

# Eliminar contenedor
docker rm traveling-api

# Eliminar imagen
docker rmi traveling-memories-api:latest
```

---

## 📊 Arquitectura de servicios

```yaml
┌─────────────────────────────────────────────┐
│          Docker Compose Network             │
│          traveling-network (bridge)         │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────┐  ┌────────────────┐  │
│  │   FastAPI API    │  │   PostgreSQL   │  │
│  │  localhost:8000  │  │ localhost:5432 │  │
│  │                  │  │                │  │
│  │  Port: 8000      │  │  Port: 5432    │  │
│  │  Health Check ✓  │  │  Health Check ✓│  │
│  │                  │  │                │  │
│  │  Hot-reload: ON  │  │  Data Volume:  │  │
│  │  (dev mode)      │  │  postgres_data │  │
│  └──────────────────┘  └────────────────┘  │
│         ▲                       ▲           │
│         └───────────────────────┘           │
│        (depends_on: healthy)                │
│                                             │
└─────────────────────────────────────────────┘
```

### Servicios

| Servicio | Imagen | Puerto | Health Check |
|----------|--------|--------|--------------|
| **api** | `python:3.12-slim` (multi-stage build) | 8000 | HTTP `/` |
| **postgres** | `postgres:16-alpine` | 5432 | `pg_isready` |

### Volúmenes

| Volumen | Tipo | Punto de montaje | Propósito |
|---------|------|------------------|-----------|
| `postgres_data` | Named Volume | `/var/lib/postgresql/data` | Persistencia de datos PostgreSQL |
| `./app` | Bind Mount | `/app/app` | Hot-reload de código (desarrollo) |
| `./DB` | Bind Mount | `/docker-entrypoint-initdb.d` | Scripts SQL iniciales |

---

## 🏥 Health Checks

Ambos servicios tienen verificaciones de salud:

### API Health Check

```bash
# Verificar manualmente
curl -i http://localhost:8000/

# Verificar estado del contenedor
docker ps --filter "name=traveling-memories-api"
```

**Configuración en Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)"
```

### PostgreSQL Health Check

```bash
# Verificar manualmente
docker-compose exec postgres pg_isready -U postgres

# Ver estado del contenedor
docker ps --filter "name=traveling-memories-db"
```

---

## 🔄 Flujo de inicialización

```
1. docker-compose up -d
   ↓
2. PostgreSQL inicia
   ├─ Lee variables de entorno
   ├─ Crea usuario 'postgres'
   ├─ Crea base de datos 'travel_db'
   └─ Ejecuta scripts en DB/ (en orden alfabético)
      ├─ create_roles_app.sql
      ├─ create_schema_travel_and_tables.sql
      ├─ insert_countries.sql
      └─ insert_into_appuser.sql
   ↓
3. API espera a que PostgreSQL esté healthy
   ├─ Instala dependencias (requirements.txt)
   ├─ Inicia FastAPI con Uvicorn
   └─ Hot-reload activado
   ↓
4. Servicios listos en:
   ├─ API: http://localhost:8000
   └─ DB: localhost:5432
```

---

## 🛠️ Troubleshooting

### "Port 8000 already in use"

```bash
# Encontrar qué procesa usa el puerto
lsof -i :8000

# Matar el proceso
kill -9 <PID>

# O usar otro puerto en docker-compose
# Cambiar en docker-compose.yml: "8001:8000"
```

### "Can't connect to PostgreSQL"

```bash
# Ver logs de postgres
docker-compose logs postgres

# Verificar health check
docker-compose ps postgres

# Reiniciar postgres
docker-compose restart postgres

# Verificar conectividad desde API
docker-compose exec api psql -h postgres -U postgres -d travel_db -c "SELECT 1;"
```

### "API returns 500 error"

```bash
# Ver logs detallados
docker-compose logs api

# Acceder al contenedor y debuggear
docker-compose exec api sh

# Verificar que requirements.txt esté instalado
docker-compose exec api pip list
```

### "Volumen PostgreSQL corrupto"

```bash
# ⚠️ Esto elimina la base de datos
docker-compose down -v

# Reiniciar limpio
docker-compose up -d
```

---

## 📦 Entornos de despliegue

### Desarrollo (Actual)

```bash
docker-compose up -d
```

**Características:**
- Hot-reload activado
- Logs detallados
- Health checks cada 10s
- Base de datos reinicializada en cada `down -v`

### Staging/Producción

Para producción, crear `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    restart: always
    environment:
      ENVIRONMENT: production
      # Usar secrets de Docker o variables externas
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    
  postgres:
    restart: always
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**Ejecutar:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔒 Seguridad

### Mejores prácticas

1. **Nunca commits `.env`** ✓ (ya está en .gitignore)
2. **Usa contraseñas fuertes** en producción
3. **Actualiza imágenes base** regularmente
   ```bash
   docker-compose pull
   docker-compose up -d --build
   ```
4. **Scannea vulnerabilidades** en imágenes
   ```bash
   docker scan traveling-memories-api:latest
   ```
5. **Usa variables de entorno** para secretos, no hardcodes
6. **Usa networks privadas** en producción
7. **Habilita HTTPS** con Nginx reverse proxy
8. **Limita recursos** (memory, CPU)

---

## 📚 Recursos útiles

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Python Docker Best Practices](https://docs.docker.com/language/python/build-images/)

---

## 🆘 Comandos de emergencia

```bash
# Limpiar TODO (contenedores, redes, volúmenes)
docker-compose down -v --remove-orphans

# Reiniciar desde cero
docker-compose up -d --build

# Ver uso de recursos
docker stats

# Inspeccionar volumen
docker volume inspect traveling-memories-backend_postgres_data

# Backup completo
docker-compose exec postgres pg_dump -U postgres travel_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Limpiar imágenes dangling
docker image prune -a
```

---

**Última actualización**: Febrero 2026  
**Versión**: 1.0.0
